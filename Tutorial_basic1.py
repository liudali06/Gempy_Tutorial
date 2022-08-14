import gempy as gp

# Importing auxiliary  libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setting options
np.random.seed(1515)
pd.set_option('precision', 2)

"""大多数数据从CSV文件形式出现的原始数据生成，
也可通过其他程序导出的模型数据或excel等软件中创建模型的数据来获得此类文件"""
"""本次实验所用数据均有CSV文件创建（数据包括X、Y、Z所有表面点和方向测量的位置值（极点、方位角和极性））"""
"""表面点还被分配一个编队，用于标记岩性单元或’主断层‘之类的构造特征"""
"""Gempy中，界面位置点标记了层的底部，如果需要模拟地层的顶部（侵入体），可以考虑定义相应的反向定向测量实现"""
"""导入数据时，必须为每个轴声明所需的分辨率，用于决定建模过程中使用的体素数量，模型范围的选择应使其包含代表性空间中的所有数据"""


geo_model = gp.create_model('Tutorial_ch1_Basics')
data_path = 'E:/Gempy/gempy_data/data/input_data/getting_started/'
# Importing the data from CSV-files and setting extent and resolution
gp.init_data(geo_model, [0, 2000., 0, 2000.,0, 750.], [50, 50, 50],
             path_o=data_path + "simple_fault_model_orientations.csv",
             path_i=data_path + "simple_fault_model_points.csv",
             default_values=True)

"""导入数据后，形成的顺序和各自的分配到的系列仍然是完全任意的，我们将通过以下方法去解决这个问题"""
"""使用pandas读取数据后，使用head函数观察一下读取的数据，head函数只能读取前五行数据"""
"""观察读取geo_model数据中的表面点数据和方向数据"""
gp.get_data(geo_model, 'surface_points').head()
gp.get_data(geo_model, 'orientations').head()

"""声明地质构造的顺序"""
"""我们希望地质单元能以正确的年龄顺序出现。
这种顺序可能是地层的沉积序列、由于侵蚀或其他岩性成因时间（如火山岩侵入）引起的不整合给出"""
"""对于我们模型中的断层，将声明一个与其年龄相关的顺序。
在Gempy中，我们使用set_series通过Python字典中的声明将编队分配给不同的顺序序列"""
"""定义正确的顺序对于模型的构建至关重要
Python>3.6,地质年龄的顺序以由关键条目的顺序定义，即第一个条目是最年轻的系列，最后一个是最老的系列。
对于旧版本的Python，则必须将正确的属性指定为单独的列表属性（order_series）"""
"""可将多个曲面分配给一个系列，系列中的单元顺序仅与颜色代码相关，建议保持一致，
该顺序可以通过另一个属性（order_formation）或使用特定的命令来定义此顺序（set_order_formation）"""
"""每个断层都被视为一个独立的系列，并且必须设置在top of the pile（堆的顶部）。
不同断层之间的相对顺序定义了它们之间的构造关系（第一个条目是最年轻的）"""
"""在简单连续地层学的模型中，所有层机构都可以分配给同一个系列。所有的单元边界及其顺序由接口点给出
然而，为了模拟更复杂的岩石地层关系和相互作用，单独系列的定义变得很重要。例如，需要声明一个’较新‘系列来扰乱旧地层的不整合或侵入"""


"""默认情况下，我们创建一个由数据推断的简单序列：
我们例子的模型主要包括四个主要层（加上一个由Gempy自动生成的底层）和一个主要的正断层置换。
假设一个简单的地层学，其中每个较年轻的单元都沉积在较老的单元上，我们可以将这些层（地层）分配
给一个名为’Start_Series‘的系列，对于断层，我们将相应的’Fault_Series‘声明为’set_series‘字典
中的第一个键条目。我们可以为这些系列赋予任何其他的名称，但是必须在输入数据中为这些编队命名
"""

"""map_stack_to_surfaces映射哪些表面属于哪个地质特征,设定字典键—值对，所属系列为主键，地层表面类型为’值‘"""
gp.map_stack_to_surfaces(geo_model,
                         {"Fault_Series":'Main_Fault',
                          "Strat_series":('Sandstone_2', 'Siltstone',
                                          'Shale', 'Sandstone_1', 'basement')},
                         remove_unused_series=True)
"""将特征设置为断层并更新模型所有的依赖对象，’Fault_Series‘指的是断层系列的名称,为属于断层的系列设置一个标志（上一步是设置键值对，但并未指明
哪个系列是断层，这条语句的目的，即在于绑定断层关系，指定'Fault_Series是断层'）"""
geo_model.set_is_fault(['Fault_Series'])


"""从我们输入的数据返回信息"""
"""我们的模型输入数据（此处命名为’geo_model‘）包含构建模型所必须的所有信息。
可通过gp.get_data使用属性或简单地访问数据来获取不同类型地信息"""

"""例如，可通过以下方式返回建模网络的坐标："""
# geo_model.grid

"""Gempy的核心算法基于两类数据的插值：—surface_points和—orientation测量"""
"""可视化输入数据"""
"""使用plot_data函数，可以将数据点二维投影到选定的’方向‘平面上。（我们可以选择此属性为x/y/z）"""
plot = gp.plot_2d(geo_model, show_lith=False, show_boundaries=False)
plt.show()

"""使用plot_Data_3D,可在3D中可视化这些数据，但Gempy中的直接3D需要安装VTK工具"""
"""GemPy中的所有3D绘图都是交互式的，意味着我们可以拖放任何数据点和测量值。  VTK中的垂直轴视图对于仅在所需的2D平面上移动点十分有用。
我们对数据的任何更改，都将永久存储在'InputData'数据框中，如果我们想要重置我们的数据点，我们将需要重新加载我们的原始输入数据"""


"""执行下面的单元格将打开一个新的窗口，其中包含我们数据的3D交互式绘图(plotter_type绘图仪款式)"""
gpv = gp.plot_3d(geo_model, image=False, plotter_type='basic')


"""模型生成"""
"""当我们确定我们在我们的对象中定义了我们想要的所有主要信息后（DataManagement、InputData）(教程中统一命名为geo_data)
便可以继续创建我们的地质模型：准备插值的输入数据"""
"""这是通过interp_dataInputData函数，从我们的对象生成一个的对象来完成的(interpolator插值器)"""
"""此步骤在于设置插值器的属性，启用模型计算所需的theano和对theano编译进行优化"""

gp.set_interpolator(geo_model, compile_theano=True,theano_optimizer='fast_compile')

"""interp_dataInputData函数重新调整原始数据的范围和坐标（并将其存为geo_data_res，作为普通属性存在在Inputdata对象中）并添加插值
所需的数学参数。这一步编译了模型计算所需的theano函数，如不需要，可在函数声明中，使用compile_theano=false进行跳过"""
"""此外，该准备过程包括为每个编队分配编号。这里需要注意，Gempy会创建一个默认的basement地层作为最后一个地层的编号。之后
编号号码按照系列和编队的顺序从最年轻到最老进行分配。根据我们插值属性的formation我们可以找出哪个数字分配给了哪个编队"""
"""用于插值的参数可以使用get_kriging_parameters函数返回，这些数据都是从原始数据自动生成的，但可以根据需要进行更改。但是，
如不是完全理解他们的意义所在，则应该小心这样做"""
gp.get_data(geo_model, 'kriging')

"""至此，我们已经拥有计算完整模型（compute_model）所需的一切。默认情况下，这将以数组的形式返回两个单独的解决方案。
第一个给出关于地层岩性的信息，第二个给出模型中关于断层网络的信息。这些数组由两个子数据组成，每个子数组作为条目"""
"""岩性块模型解决方案：条目①：该数组显示在每个体素中发现了哪种岩性地层，如对应的地层编号所示。
                    条目②：表示块模型中岩性单元和层的方向的势场阵列"""
"""断层网络块模型解决方案。条目①：该数组表示断层分离区域由每个体素中包含的不同数字表示
                    条目②：块模型中与断层网络相关的势场数组"""


"""下面，将说明不同的模型解决方案以及如何使用它们"""
sol = gp.compute_model(geo_model)

"""GemPy中的直接模型可视化"""
"""模型解决方案可以在Gempy的2D部分轻松可视化，下面浏览一下岩性块："""
gp.plot_2d(geo_model, show_data=True)
plt.show()

"""show_scalar表示显示标量场的等值线，默认为假，此时模型的岩性分层情况将按照模型输入数据进行分配；当等值线为假时，模型便不会根据实际情况显示地形的特征；
   show_lith表示显示岩性块的体积，默认为真，当不显示岩性块的体积时，模型实际显示情况将随机进行分配，不按照实际情况"""
gp.plot_2d(geo_model, show_data=False, show_scalar=True,show_lith=False)
plt.show()

"""此处的series_n=1 表示指明了岩性单元和层的方向，相较于上方的图像展示，结果出现了明显按照线性分层的图形；
   这很好的说明了地层雨褶皱相关的便些，以及地层受断层影响的方式"""
gp.plot_2d(geo_model, series_n=1, show_data=False, show_scalar=True, show_lith=False)
plt.show()


"""断层网络建模解决方案可以以相同的方式可视化"""
geo_model.solutions.scalar_field_at_surface_points
"""当show_block为真，且已经计算了相关模型之后，将绘制最终模型的横截面；
   show——lith代表是否显示岩性块的体积，默认为真"""
gp.plot_2d(geo_model, show_block=True, show_lith=False)
plt.show()

"""此处添加了series_n=1表示显示岩性单元和层的方向"""
gp.plot_2d(geo_model, series_n=1, show_block=True, show_lith=False)
plt.show()



"""进行立方体和VTK可视化操作"""
"""除了2D部分，我们还可以提取表面在3D渲染器中进行可视化。曲面可以在VTK中可视化为3D三角形复合体（见plot_surface_3D函数）
为了创建这些三角形，我们需要从岩性和断层的潜在场中提取各自相应的顶点和单纯形"""
ver, sim = gp.get_surfaces(geo_model)
"""执行下面的单元格将打开一个新的窗口，其中包含我们数据的3D交互式绘图(plotter_type绘图仪款式)"""
gpv = gp.plot_3d(geo_model, image=False,plotter_type='basic')

"""使用重新缩放的插值数据，使得我们可以在交互模式下运行我们的3D VTK可视化。允许我们实时更改和更新我们的模型，该模型与输入数据时的
   交互式3D可视化类似，更改之后会永久保存。此外，更改模型时产生的变化也将被重新实时计算"""

"""添加地形"""
"""创建一个地形网格并激活，d_z表示最大高度差，如果没有，则在Z方向上最后20%的模型"""
geo_model.set_topography(d_z=(350,750))

gp.compute_model(geo_model)
gp.plot_2d(geo_model, show_topography=True)
plt.show()


#sphinx_gallert_thumbnail_number = 9
gpv = gp.plot_3d(geo_model, plotter_type='basic', show_topography=True, show_surfaces=True,
                 show_lith=True,image=False)


"""保存模型"""
"""Gempy使用Python快速存储临时对象。但是需要模块版本一致性。要将pickle加载到Gempy中，必须保证使用与最初存储数据时使用的相同版本的
pickle和依赖模块（如：Pandas和Numpy）"""
"""为了长期存储，我们可以使用padas。Datafrom方法将其导出到CSV"""
gp.save_model(geo_model)