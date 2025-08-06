# build/test
git clone https://github.com/rgbforge/hybridoctree.git

mkdir build && cd build

cmake ..

make

mv ../inputs/model.* .

./Hexgen ./model.stl



# Kokkos HybridOctree_Hex
A fork of [HybridOctree_Hex](https://github.com/CMU-CBML/HybridOctree_Hex) focused on developing a kokkos backend

HybridOctree_Hex received the best technical poster award in [the 2024 International Meshing Roundtable](https://internationalmeshingroundtable.com/awards/).

## Original Author and Citation

[![DOI](https://img.shields.io/badge/DOI-10.1016/j.jocs.2024.102278-blue)](https://doi.org/10.1016/j.jocs.2024.102278)

```angular2html
@article{tong2024hybridoctree_hex,
  title={HybridOctree\_Hex: Hybrid octree-based adaptive all-hexahedral mesh generation with Jacobian control},
  author={Tong, Hua and Halilaj, Eni and Zhang, Yongjie Jessica},
  journal={Journal of Computational Science},
  volume={78},
  pages={102278},
  year={2024},
  publisher={Elsevier}
}
`
