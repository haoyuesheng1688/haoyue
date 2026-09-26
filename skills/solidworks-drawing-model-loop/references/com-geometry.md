# COM 与几何接口要点

## 连接、无参成员和类型包装

`scripts/sw_probe.py` 提供 ROT 绑定。通用 ProgID 可能对应其他安装版本，以实际进程和 `RevisionNumber` 确定版本。

pywin32 动态包装会把部分无参方法暴露为属性；COM 返回对象本身也可能 callable：

```python
def value(obj, name):
    member = getattr(obj, name)
    if hasattr(member, '_oleobj_'):
        return member
    return member() if callable(member) else member
```

用于实际遇到的 `FirstFeature`、`GetNextFeature`、`GetFaces`、`GetBody`、`GetEquationMgr`、`CreateMassProperty` 等无参访问。具体失败先查签名，不给所有成员盲加括号。

需要类型包装时从当前类型库取版本，不固定34：

```python
attr = pythoncom.LoadTypeLib(tlb_path).GetLibAttr()
lib = win32com.client.gencache.EnsureModule(attr[0], attr[1], attr[3], attr[4])
part = lib.IPartDoc(model._oleobj_.QueryInterface(
    lib.IPartDoc.CLSID, pythoncom.IID_IDispatch))
```

第二个 `IID_IDispatch` 参数解决过 `There is no interface object registered that supports this IID`。该会话 `CastTo` 也曾无法自动生成包装；上述显式查询成功。

空 COM 对象用 `VARIANT(VT_DISPATCH, None)`。SaveAs 错误/警告用 `VARIANT(VT_BYREF | VT_I4, 0)`，文件出现不代替状态检查。

## 草图变换和方向

枚举 `GetTypeName2 == 'RefPlane'` 取得真实名称；不要硬编码英文平面名称，也不能假设任意文档所有基准面的顺序相同。

本次默认模板的 `ModelToSketchTransform` 前9项及模型点到草图点映射：

| 平面 | 前9项 | 映射 |
|---|---|---|
| Top | 1,0,0, 0,0,1, 0,-1,0 | (x,-z,y) |
| Right | 0,0,1, 0,1,0, -1,0,0 | (-z,y,x) |

Top 局部正Y对应全局负Z，草图法向对应全局正Y。因此直接把全局Z写成草图Y会把入口放到相反侧。

优先用 MathPoint/MathTransform 转换，必要时按当前矩阵定义手算并验证点的往返。本次创建视图变换需要显式 double SAFEARRAY；裸 list 曾未得到预期视图：

```python
data = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, doubles)
transform = math_utility.CreateTransform(data)
```

`FeatureExtrusion2.Dir` 与 `FlipStartOffset` 分别控制延伸与起始偏移；凸台与 `FeatureCut3` 默认方向也不能混为一谈。可用 `IExtrudeFeatureData2.ReverseDirection`、`FromOffsetReverse`、`FromOffsetDistance` 修正并 `ModifyDefinition`，随后重建实测。

本模板中，Top平面正Y凸台使用 `Dir=False`、`FlipStartOffset=False`；Front平面负Z入口法兰需要负向起始偏移和负向延伸。此为该模板实测，不是跨模板常量。

退出新建草图后且未插入其他特征时，`FeatureByPositionReverse(0)` 曾用于取得草图命名；先核对确为草图，不作为长流程中通用目标查询。

## 薄壳、孔组与材料

锥壳内半径随高度的斜率为k、法向厚度为t，同一轴向高度处径向差为 `t*sqrt(1+k*k)`。端部连接与切平面另按图纸解释。输入可用mm，API几何通常用m，显式转换。

`FeatureRevolve2` 的闭合环截面和中心线可生成独立实体。Merge设置决定是否合并，不能把多实体等同组件装配。

案例中出口6孔从底部平面贯穿时误伤锥壳与顶盖；改为在出口法兰顶端面建草图，按法兰厚度有限切除后锥壳体积恢复。最终检查孔径、数量、受影响面和目标实体。

`InsertMoveCopyBody2` 的实体选择标记为1、旋转参考为2。平移与旋转不应在同一次调用中都被假设生效。

英文 `AISI Type 316L stainless steel` 本次设置后回读为空；中文版库 `AISI 类型 316L 不锈钢` 成功。确切原因未证实，不写成普遍规律。从实际 `lang/<language>/sldmaterials/*.sldmat` 查询名称并回读结果；无返回值的Set方法不是成功证明。实体级材料覆盖需另行检查。

## 验证结果的含义

- `IBody2.GetMassProperties(1.0)[3]` 为m³体积；密度1仅用于几何检查，不能据此报钢件真实质量。
- `GetBodyBox` 是近似范围且可能随重建改变，适合发现正负方向和数量级错误，不能检查精密尺寸。
- 类型化 `IFeature.GetErrorCode2()` 包含错误码和是否警告；顶层检查不能代替子特征或完整设计检查。
- 重开比较数量、体积、材料和关键参数；用合理容差，不可读状态报告未知。
- 当前快照不会主动重建，因此不能称为完成过重建验证。

## 官方依据

- [旋转示例](https://help.solidworks.com/2025/English/api/sldworksapi/Create_Revolve_Features_Example_VB.htm)
- [swStartOffset=3](https://help.solidworks.com/2024/english/api/swconst/SOLIDWORKS.Interop.swconst~SOLIDWORKS.Interop.swconst.swStartConditions_e.html)
- [移动/复制与选择标记](https://help.solidworks.com/2020/English/api/sldworksapi/SOLIDWORKS.Interop.sldworks~SOLIDWORKS.Interop.sldworks.IFeatureManager~InsertMoveCopyBody2.html)
- [实体质量属性与密度参数](https://help.solidworks.com/2024/english/api/sldworksapi/SolidWorks.Interop.sldworks~SolidWorks.Interop.sldworks.IBody2~GetMassProperties.html)
- [包围盒的近似性质](https://help.solidworks.com/2026/english/api/sldworksapi/SolidWorks.Interop.sldworks~SolidWorks.Interop.sldworks.IBody2~IGetBodyBox.html)
