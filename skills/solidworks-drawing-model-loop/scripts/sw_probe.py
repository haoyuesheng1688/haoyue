"""Read-only SolidWorks inventory and explicitly targeted part snapshot.

Requires Windows and pywin32. Never launches, activates, rebuilds or saves CAD.
--tlb may generate pywin32 wrappers; --output creates a new JSON report.
"""
import argparse
import json
import math
import os
from pathlib import Path
import sys


def value(obj, name):
    member = getattr(obj, name)
    if hasattr(member, '_oleobj_'):
        return member
    return member() if callable(member) else member


def running(pythoncom, client):
    rot = pythoncom.GetRunningObjectTable()
    context = pythoncom.CreateBindCtx(0)
    result = []
    for moniker in rot.EnumRunning():
        name = moniker.GetDisplayName(context, None)
        if name.startswith('SolidWorks_PID_') and name.rsplit('_', 1)[-1].isdigit():
            app = client.Dispatch(rot.GetObject(moniker).QueryInterface(pythoncom.IID_IDispatch))
            result.append((int(name.rsplit('_', 1)[-1]), app))
    return sorted(result, key=lambda item: item[0])


def identity(model):
    return {'title': value(model, 'GetTitle'), 'path': value(model, 'GetPathName'),
            'type': value(model, 'GetType')}


def snapshot(model, lib, pythoncom):
    result = identity(model)
    if result['type'] != 1:
        raise ValueError('Part snapshots only; assemblies need component-specific verification')
    bodies = []
    for body in model.GetBodies2(0, False) or []:
        props = body.GetMassProperties(1.0)
        if props is None or len(props) < 5:
            raise ValueError('Body mass properties unavailable')
        volume = float(props[3])
        if not math.isfinite(volume) or volume <= 0:
            raise ValueError('Non-positive or non-finite solid volume')
        bodies.append({'name': body.Name, 'faces': len(value(body, 'GetFaces') or []),
                       'volume_m3': volume, 'area_m2': props[4],
                       'approximate_bounds_m': value(body, 'GetBodyBox')})
    result.update(body_count=len(bodies), bodies=bodies,
                  total_volume_m3=sum(b['volume_m3'] for b in bodies),
                  note='Read-only current state; no rebuild, interference or dimensional acceptance performed')
    if lib is None:
        result['typed_checks'] = 'unavailable: pass --tlb for material and top-level feature status'
        return result
    part = lib.IPartDoc(model._oleobj_.QueryInterface(lib.IPartDoc.CLSID, pythoncom.IID_IDispatch))
    result['material'] = part.GetMaterialPropertyName2('')
    result['feature_check_scope'] = 'top-level only, current rebuild state'
    result['features'] = []
    feat = value(model, 'FirstFeature')
    while feat:
        status = lib.IFeature(feat._oleobj_).GetErrorCode2()
        result['features'].append({'name': feat.Name, 'type': value(feat, 'GetTypeName2'),
                                   'code': status[0], 'is_warning': bool(status[1])})
        feat = value(feat, 'GetNextFeature')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, help='Observed SolidWorks PID for multi-instance snapshots')
    parser.add_argument('--document', help='Absolute path of an already-open part; no ActiveDoc fallback')
    parser.add_argument('--tlb', help='Installed sldworks.tlb for typed material/feature readback')
    parser.add_argument('--output', type=Path, help='New JSON report, refuses replacement')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('Output exists; choose a new report path')
    if args.document and not os.path.isabs(args.document):
        parser.error('--document must be absolute')
    import pythoncom
    import win32com.client as client
    pythoncom.CoInitialize()
    try:
        instances = running(pythoncom, client)
        if args.pid is not None:
            instances = [item for item in instances if item[0] == args.pid]
            if not instances:
                raise ValueError('Requested PID not registered in ROT')
        if not args.document:
            report = {'instances': []}
            for pid, app in instances:
                docs = value(app, 'GetDocuments') or []
                report['instances'].append({'pid': pid, 'revision': value(app, 'RevisionNumber'),
                                            'documents': [identity(doc) for doc in docs]})
        else:
            if len(instances) != 1:
                raise ValueError('Need exactly one instance; inspect inventory and specify --pid')
            pid, app = instances[0]
            model = app.GetOpenDocumentByName(args.document)
            if model is None:
                raise ValueError('Requested file not open; no document opened or modified')
            actual = value(model, 'GetPathName')
            if os.path.normcase(os.path.normpath(actual)) != os.path.normcase(os.path.normpath(args.document)):
                raise ValueError('Document identity mismatch')
            lib = None
            if args.tlb:
                attr = pythoncom.LoadTypeLib(str(Path(args.tlb).resolve(strict=True))).GetLibAttr()
                lib = client.gencache.EnsureModule(attr[0], attr[1], attr[3], attr[4])
            report = {'pid': pid, 'revision': value(app, 'RevisionNumber'),
                      'snapshot': snapshot(model, lib, pythoncom)}
        encoded = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(encoded + '\n')
        print(encoded)
    finally:
        pythoncom.CoUninitialize()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
