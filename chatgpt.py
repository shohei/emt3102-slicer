import struct
import numpy as np
import matplotlib.pyplot as plt
import pdb
from scipy.spatial import ConvexHull
import k3d
import time

def read_binary_stl(filename):
    with open(filename, "rb") as f:
        # 80バイトのヘッダーをスキップ
        header = f.read(80)
        print("Header:", header.decode(errors="ignore"))

        # 4バイトの三角形数を取得
        num_triangles = struct.unpack("<I", f.read(4))[0]
        print("Number of triangles:", num_triangles)

        triangles = []

        for _ in range(num_triangles):
            # 1つの三角形のデータ（50バイト）
            data = f.read(50)

            # 法線ベクトル (3 x float32)
            normal = struct.unpack("<fff", data[0:12])

            # 3つの頂点座標 (3 x (3 x float32))
            v1 = struct.unpack("<fff", data[12:24])
            v2 = struct.unpack("<fff", data[24:36])
            v3 = struct.unpack("<fff", data[36:48])

            # 2バイトの属性バイト数（無視する）
            attr_byte_count = struct.unpack("<H", data[48:50])[0]

            triangles.append((normal, v1, v2, v3))

        return triangles

# 例：STLファイルを読み込んで表示
stl_file = "your_file.stl"
triangles = read_binary_stl(stl_file)

xs = np.array([])
ys = np.array([])
zs = np.array([])
if triangles:
    for t in triangles:
        print ("Triangle #", triangles.index(t))
        print("  Normal:", t[0])
        print("  Vertex 1:", t[1])
        print("  Vertex 2:", t[2])
        print("  Vertex 3:", t[3])
        # pdb.set_trace()
        xs = np.append(xs,t[0][0])
        xs = np.append(xs,t[0][1])
        xs = np.append(xs,t[0][2])
        ys = np.append(ys,t[1][0])
        ys = np.append(ys,t[1][1])
        ys = np.append(ys,t[1][2])
        zs = np.append(zs,t[2][0])
        zs = np.append(zs,t[2][1])
        zs = np.append(zs,t[2][2])

zrange = np.linspace(zs.min(),zs.max(),5) 
for zp in zrange:
    # plt.figure()
    plot = k3d.plot()
    # plot.display()
    points = np.zeros([1,3])
    for t in triangles:
        first = t[0]
        second = t[1]
        third = t[2]
        x1 = first[0]
        x2 = second[0]
        x3 = third[0]
        y1 = first[1]
        y2 = second[1]
        y3 = third[1]
        z1 = first[2]
        z2 = second[2]
        z3 = third[2]
        if zp > z1 and zp < z2:
            k = (zp-z1)/(z2-zp)
            x = 1/(1+k)*x1 + k/(1+k)*x2
            y = 1/(1+k)*y1 + k/(1+k)*y2
            # x = x1 + (x2 - x1) * (zp - z1) / (z2 - z1)
            # y = y1 + (y2 - y1) * (zp - z1) / (z2 - z1)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp > z2 and zp < z3:
            k = (zp-z2)/(z3-zp)
            x = 1/(1+k)*x2 + k/(1+k)*x3
            y = 1/(1+k)*y2 + k/(1+k)*y3
            # x = x2 + (x3 - x2) * (zp - z2) / (z3 - z2)
            # y = y2 + (y3 - y2) * (zp - z2) / (z3 - z2)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp > z3 and zp < z1:
            k = (zp-z3)/(z1-zp)
            x = 1/(1+k)*x3 + k/(1+k)*x1
            y = 1/(1+k)*y3 + k/(1+k)*y1
            # x = x3 + (x1 - x3) * (zp - z3) / (z1 - z3)
            # y = y3 + (y1 - y3) * (zp - z3) / (z1 - z3)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp > z2 and zp < z1:
            k = (zp-z2)/(z1-zp)
            x = 1/(1+k)*x2 + k/(1+k)*x1
            y = 1/(1+k)*y2 + k/(1+k)*y1
            # x = x2 + (x1 - x2) * (zp - z2) / (z1 - z2)
            # y = y2 + (y1 - y2) * (zp - z2) / (z1 - z2)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp > z3 and zp < z2:
            k = (zp-z3)/(z2-zp)
            x = 1/(1+k)*x3 + k/(1+k)*x2
            y = 1/(1+k)*y3 + k/(1+k)*y2
            # x = x3 + (x2 - x3) * (zp - z3) / (z2 - z3)
            # y = y3 + (y2 - y3) * (zp - z3) / (z2 - z3)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp > z1 and zp < z3:
            k = (zp-z1)/(z3-zp)
            x = 1/(1+k)*x1 + k/(1+k)*x3
            y = 1/(1+k)*y1 + k/(1+k)*y3
            # x = x1 + (x3 - x1) * (zp - z1) / (z3 - z1)
            # y = y1 + (y3 - y1) * (zp - z1) / (z3 - z1)
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp == z1:
            x = x1
            y = y1
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp == z2:
            x = x2
            y = y2
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
        elif zp == z3:
            x = x3
            y = y3
            points = np.vstack([points,np.array([x,y,zp])])
            # plt.plot(x,y,'ro')
            # print("x:", x, "y:", y, "z:", zp)
    plot +=k3d.points(points, point_size=0.02, color = 0xff00ff)
    print(points)
    try:
        hull = ConvexHull(points)
        print(hull)
        for simplex in hull.simplices:
            plot +=k3d.points(points[simplex], point_size=0.02, color = 0x0000ff)
            plot +=k3d.line(points[simplex], point_size=0.02, color = 0x0000ff)
        plot.display()
    except Exception:
        pass
# plt.show()


