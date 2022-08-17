#importing Gempy
import gempy as gp

#importing auxiliary libraries
import numpy as np
import pandas as pd

"""系列定义"""
"""Series是包含每个独立标量字段关联的属性的对象。当下它只代表系列的顺序（由索引顺序推断）。之后会添加不整合关系或可能的
插值器类型"""
"""Series类和Fault类的关系十分微妙，因为fault是series的视图"""
faults = gp.Faults()
series = gp.Series(faults)


"""我们可以用set_series_index方法去修改series"""
series.set_series_index(['foo', 'foo1', 'foo5','foo7'])
"""Series的索引是pandas类别"""
"""添加新的系列"""
series.add_series('foo3')
"""删除系列"""
series.delete_series('foo3')
"""重命名系列"""
series.rename_series({'foo':'boo'})


"""断层"""
"""df断层用于表示那些数学series表现为断层。如果提到的断层是有限或无限时，当我们修改链接到断层对象的series对象时，
两个数据帧都会自动更新（通过再创建系列对象时传递它）"""
"""我们可以使用set_is_falut方法去选择我们的series中的哪些是断层"""
faults.set_is_fault(['boo'])

fr = np.zeros((4,4))
fr[2,2] = True
fr[1,2] = True
faults.set_fault_relation(fr)

"""现在，如果我们更改series DF并更新已定义的系列将保留其值，而性的series将被设置为false"""
series.add_series('foo20')

"""当我们添加新的series时，值会切换成NaN。因此，我们要小心再DF中没有任何的NaN,否则将引发错误。"""


"""Surfaces"""
"""DF曲面包含三个属性，ID是指连续堆表面的顺序，即严格的计算顺序。另一方面，值是离散化后每个体素将具有的最终值。
例如，在我们想要将特定的地球物理属性（例如密度）映射到给定单位的情况下，这是非常有用的。
在默认情况下，两者是相同的，因为离散岩性单元的值是人影的"""
"""Surfaces类需要一个关联的series对象，这将会限制series 的名称"""
surfaces = gp.Surfaces(series)
"""我们可以通过传递带有名称的列表去设置任意数量的编队。在默认情况下，它们将采用名称或第一个series"""
surfaces.set_surfaces_names(['foo', 'foo2', 'foo5'])
"""添加新的表面编队"""
surfaces.add_surface(['foo6'])

"""设置相关值"""
"""设置相关值我们使用set_surfaces_values方法进行"""
surfaces.set_surfaces_values([2, 2, 2, 5])

"""使用给定的名称设置值"""
"""我们可以给属性指定特定的名称(即密度)"""
surfaces.add_surfaces_values([[2, 2, 2, 6],[2, 2, 1, 8]], ['val_foo','val2_foo'])

"""删除编队值"""
"""删除完整的属性"""
surfaces.delete_surface_values(['val_foo','value_0'])

"""必须将其中一种结构设置为Basement"""
surfaces.set_basement()

"""设置阵列的值"""
"""我们可以使用set_surface_values代替添加，这会删除之前的属性并添加新的属性"""
surfaces.set_surfaces_values([[2, 2, 2, 6],[2, 2, 1, 8]], ['val_foo','val2_foo'])

"""将series映射到地层"""
"""将一个series映射到一个编队，可以通过传递一个dict来实现"""
"""如果对象不存在系列Seires，将会发出警告，并将这些编队设置为NaNS"""
d = {"foo7": 'foo', "booX":('foo2', 'f225,', 'fee' )}
surfaces.map_series(d)
"""类别的一个优点在于它们是有序的，所以可以通过series和formation去整理DF"""

"""修改表面的名称"""
surfaces.rename_surfaces({'foo2': 'lala'})
surfaces.df.loc[2,'val_foo'] = 22


"""表面DF包含一个用于显示表面颜色的列，在需要更改颜色时可以今天调用"""
surfaces.colors.change_colors()
"""在已知想要使用的颜色时，可以使用表面的名称通过十六进制颜色字符串的字典来更新它们"""
new_color = {'foo': '#ff8000', 'foo5': '#4741be'}


"""数据的处理"""
"""表面点"""


