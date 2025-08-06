#include <fstream>
#include <vector>
#include "Stl.h"

struct StlTriangle {
    float normal[3];
    float v1[3];
    float v2[3];
    float v3[3];
    unsigned short attributeByteCount;
};

bool ReadStl(const char* fileName, Mesh& triMesh) {
    std::ifstream file(fileName, std::ios::in | std::ios::binary);
    if (!file) {
        std::cerr << "error: can't open file" << fileName << std::endl;
        return false;
    }

    char header[80];
    file.read(header, 80);
    unsigned int numTriangles;
    file.read(reinterpret_cast<char*>(&numTriangles), sizeof(unsigned int));
    if (numTriangles == 0) {
        std::cerr << "error: no triangles" << std::endl;
        return false;
    }

    std::vector<std::vector<double>> vertices;
    std::vector<std::vector<int>> faces;
    faces.resize(numTriangles);
    for (unsigned int i = 0; i < numTriangles; ++i) {
        StlTriangle tri;
        file.read(reinterpret_cast<char*>(&tri), sizeof(StlTriangle));
        float v[3][3] = {
            {tri.v1[0], tri.v1[1], tri.v1[2]},
            {tri.v2[0], tri.v2[1], tri.v2[2]},
            {tri.v3[0], tri.v3[1], tri.v3[2]}
        };

        faces[i].resize(3);
        for (int j = 0; j < 3; ++j) {
            bool found = false;
            for (size_t k = 0; k < vertices.size(); ++k) {
                if (vertices[k][0] == v[j][0] && vertices[k][1] == v[j][1] && vertices[k][2] == v[j][2]) {
                    faces[i][j] = k;
                    found = true;
                    break;
                }
            }
            if (!found) {
                std::vector<double> new_v = { (double)v[j][0], (double)v[j][1], (double)v[j][2] };
                vertices.push_back(new_v);
                faces[i][j] = vertices.size() - 1;
            }
        }
    }

    file.close();
    triMesh.Initialize(numTriangles, vertices.size(), 3);
    triMesh.eNum = numTriangles;
    triMesh.vNum = vertices.size();
    for (size_t i = 0; i < vertices.size(); ++i) {
        triMesh.v[i][0] = vertices[i][0];
        triMesh.v[i][1] = vertices[i][1];
        triMesh.v[i][2] = vertices[i][2];
    }
    for (unsigned int i = 0; i < numTriangles; ++i) {
        triMesh.e[i][0] = faces[i][0];
        triMesh.e[i][1] = faces[i][1];
        triMesh.e[i][2] = faces[i][2];
    }
    return true;
}
