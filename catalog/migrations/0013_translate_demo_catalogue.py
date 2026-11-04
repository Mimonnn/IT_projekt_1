"""Zamrożone angielskie treści ofert demo; nie nadpisujemy własnych tekstów źródłowych."""
import hashlib

from django.db import migrations

DATA = {'products': [{'slug': 'narty-alpine-172',
               'category': 'skis',
               'values': {'description_en': 'Piste skis with bindings for practising turns and spending a full day on groomed slopes.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Alpine 172 variant is size 172 cm. Length: 172 cm; sidecut tip / waist / tail: 122 '
                                            '/ 73 / 106 mm. Weight: 4120 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 172 cm; sidecut tip / waist / tail: 122 / 73 / 106 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '172 cm'},
               'fingerprints': {'description': 'b7a763438fe9549b30329da7a3e2a0315ac99b636740b5505c0e01a3fadcbca0',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': '37414ef591126f055443ab9e2700c0041b3f70daeae042fe08ae17201f76e373',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'd963cf0ec1f39b8c3486f44c5dc4add576437a67370992de5de33d90dc425f72'}},
              {'slug': 'narty-traverse-84',
               'category': 'skis',
               'values': {'description_en': 'Versatile all-mountain skis with bindings for piste runs and variable snow conditions.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Traverse 84 variant is size 174 cm. Length: 174 cm; sidecut tip / waist / tail: 126 '
                                            '/ 84 / 110 mm. Weight: 4240 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 174 cm; sidecut tip / waist / tail: 126 / 84 / 110 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '174 cm'},
               'fingerprints': {'description': '3eafd84379bb8e6baaa47026825eaf9a5641cb68c56637ab7fac506b5aea1486',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': '5a37d26259cd074f9c57da4729e7ce2ae8647a60675fc4627cf4bf1abcf2e1f1',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'dbfcbb95873a520a24ac39e2bf03523590c402232e2f62d416904519d7731f16'}},
              {'slug': 'narty-ascend-102',
               'category': 'skis',
               'values': {'description_en': 'Touring skis with bindings and skins for climbing and skiing in mountain terrain.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. Carbon fibre stiffens the lightweight body. The Ascend 102 variant is size 178 cm. '
                                            'Length: 178 cm; sidecut tip / waist / tail: 134 / 102 / 121 mm. Weight: 3480 g (pair of skis '
                                            'with bindings and skins).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base. Carbon fibre stiffens the lightweight body.',
                          'dimensions_en': 'Length: 178 cm; sidecut tip / waist / tail: 134 / 102 / 121 mm.',
                          'weight_scope_en': 'pair of skis with bindings and skins',
                          'size_en': '178 cm'},
               'fingerprints': {'description': '5735d15d414eddd9cc5fe8ab58c5970ccee185e101943cbcf9d760a7afd54f46',
                                'construction': '22c61e7c2af786a707fa399626fca9d320018cfb5721432569a2600b85b4faf2',
                                'dimensions': '67f7180a1d4deb59a73ebc71346aed4c8a6cda4753c071c40ec257401c5265f4',
                                'weight_scope': '9abdd8cfc3199d8f7222e01c293a936aa667b20a3bceb329fb1fec4f6b17738c',
                                'size': 'adbec4fafb440d368a2e03814c25c10312c191c9d19cec05f2b9b896044b8973'}},
              {'slug': 'snowboard-drift-156',
               'category': 'snowboards',
               'values': {'description_en': 'An all-mountain snowboard for piste runs and exploring beyond the slopes. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Drift 156 variant is size 156 cm. Length: 156 cm; '
                                            'waist width: 25.2 cm. Weight: 2880 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 156 cm; waist width: 25.2 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '156 cm'},
               'fingerprints': {'description': 'c1cf33adb178e51177189ce2fb6d6dc3f83962083fc16033890e87cf8944207a',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': '00afd9b3a1d59bce0081ac15b0e431f65969566858e1ec701cf8736efaef0470',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '9aeaebf33d572fe524cf8959a96c5ba5ce983ab1dd56913b4341d85c42ed86dc'}},
              {'slug': 'snowboard-orbit-152',
               'category': 'snowboards',
               'values': {'description_en': 'A freestyle snowboard for tricks, jumps and riding in the snowpark. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Orbit 152 variant is size 152 cm. Length: 152 cm; '
                                            'waist width: 25.2 cm. Weight: 2760 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 152 cm; waist width: 25.2 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '152 cm'},
               'fingerprints': {'description': 'd6c2cac1672965fc72f90d01d682fe3b107edcc4b0f17523b9e1fbb7facf5977',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': '157a6950ac6f67fb7d794fe358334125bd8d3a656eda651f55b2b7ac020f80ef',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '4e79ee435a33a14fd4473879560127e9e3d3ef80ecf4a081fce03073f7413b4b'}},
              {'slug': 'snowboard-glacier-158',
               'category': 'snowboards',
               'values': {'description_en': 'A freeride snowboard for soft snow and riding beyond groomed runs. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Glacier 158 variant is size 158 cm. Length: 158 cm; '
                                            'waist width: 26.1 cm. Weight: 2940 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 158 cm; waist width: 26.1 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '158 cm'},
               'fingerprints': {'description': '94a83d355d0ba7c7aff9cd00df22fe207f9643b3694a0c4cbff61d665eff358f',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': 'a8d9090fa897d4169b88b9adffc2a224ce9276486a6e12551ff0da89b93eb4a5',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '33ed105afdf9a4253e76414ce1e32e3b0d60c5593129de2e257aa36498b4e58b'}},
              {'slug': 'wiazania-latch-junior',
               'category': 'bindings',
               'values': {'description_en': 'Junior alpine ski bindings for piste skiing. Match the boot sole length and brake width to '
                                            'your equipment.\n'
                                            '\n'
                                            'A polyamide body, steel release mechanism and aluminium rail components. Toe and heel pieces '
                                            'form a set for a pair of skis. The Latch Junior variant is size Junior (sole 200–300 mm). '
                                            'Sole length range: 200–300 mm; brake width: 76 mm. Weight: 900 g (pair of bindings).',
                          'construction_en': 'A polyamide body, steel release mechanism and aluminium rail components. Toe and heel pieces '
                                             'form a set for a pair of skis.',
                          'dimensions_en': 'Sole length range: 200–300 mm; brake width: 76 mm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'Junior (sole 200–300 mm)'},
               'fingerprints': {'description': '3fcd4a0cc4da880c5f364bbf6194cbb72a93cc84201a3e9853e8cbd93b0ea5c5',
                                'construction': 'd9b19017456d3dd402fade9b45451f31f7f5c28e8d68324b86d75ceff47ecd40',
                                'dimensions': 'e92944916545491b66b9fa597cd734febc1e6800d4df00145fcdf147a7b6c784',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': '601428f96e4bc38e5aa69c4bf53d2fec00ac63e66961d7960132fec97c5ac7ff'}},
              {'slug': 'wiazania-anchor-500',
               'category': 'bindings',
               'values': {'description_en': 'Strap snowboard bindings for all-mountain and freestyle riding. Choose the binding size to '
                                            'match your boots.\n'
                                            '\n'
                                            'A polyamide base and highback, aluminium buckles and cushioning EVA pads. Two straps hold the '
                                            'boot in the binding. The Anchor 500 variant is size M (EU 39–43). Base: 26 × 15 cm; highback '
                                            'height: 26 cm. Weight: 1800 g (pair of bindings).',
                          'construction_en': 'A polyamide base and highback, aluminium buckles and cushioning EVA pads. Two straps hold '
                                             'the boot in the binding.',
                          'dimensions_en': 'Base: 26 × 15 cm; highback height: 26 cm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'M (EU 39–43)'},
               'fingerprints': {'description': '1888a1c1a34b7faa363537f0674460806062080a9237a90cc468b118c1728616',
                                'construction': '657bf4bb7840aff8839570e6044c3afc9390d59eda4b016a236d6fa365114d54',
                                'dimensions': '57b7cb6eeb0a4ae2bfa272841dbadc7eeeeb043e87739d4dd13f2784e363d150',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': 'c08dd4e1ba984d9409474c3b82b32b08ee61ea95254cdf3c2d63c3657f3141b3'}},
              {'slug': 'wiazania-swift-360',
               'category': 'bindings',
               'values': {'description_en': 'Quick-entry snowboard bindings with a rear-opening highback for easier boot entry.\n'
                                            '\n'
                                            'A polyamide base and highback, aluminium buckles and cushioning EVA pads. A rear-opening '
                                            'highback makes boot entry easier. The Swift 360 variant is size M (EU 39–43). Base: 26 × 15 '
                                            'cm; highback height: 26 cm. Weight: 1800 g (pair of bindings).',
                          'construction_en': 'A polyamide base and highback, aluminium buckles and cushioning EVA pads. A rear-opening '
                                             'highback makes boot entry easier.',
                          'dimensions_en': 'Base: 26 × 15 cm; highback height: 26 cm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'M (EU 39–43)'},
               'fingerprints': {'description': 'edd6dcb0762e3ee14f0ecd35c38547320fded9a3a5485e00c339d535c76bef4e',
                                'construction': 'abbb2c53e13fef07cc155446801ea109e81161fd619095bb441740fc8b30b2df',
                                'dimensions': '57b7cb6eeb0a4ae2bfa272841dbadc7eeeeb043e87739d4dd13f2784e363d150',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': 'c08dd4e1ba984d9409474c3b82b32b08ee61ea95254cdf3c2d63c3657f3141b3'}},
              {'slug': 'kask-ridge-m',
               'category': 'helmets',
               'values': {'description_en': 'A classic helmet for recreational skiing and snowboarding. Choose the size to match your head '
                                            'circumference.\n'
                                            '\n'
                                            'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                            'comfort and makes cleaning easier. The Ridge M variant is size M (55–59 cm). Head '
                                            'circumference: 55–59 cm; external dimensions: 27 × 23 × 24 cm. Weight: 450 g (one helmet).',
                          'construction_en': 'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                             'comfort and makes cleaning easier.',
                          'dimensions_en': 'Head circumference: 55–59 cm; external dimensions: 27 × 23 × 24 cm.',
                          'weight_scope_en': 'one helmet',
                          'size_en': 'M (55–59 cm)'},
               'fingerprints': {'description': '4c6e743c50640f7faf72a34f1338ad4d82f1f02d9496436471615d663e2c38c1',
                                'construction': 'bc95272f515ae039ff3d1ec028a2e914fc51c91aebd56a789d657004fc9d35ae',
                                'dimensions': '181b7abd7405d91a12f83ca4f36473ae6a45e3998bba740d15f498020004f5c5',
                                'weight_scope': '89c83308b6b470141aba383066e5afc33ee7e9108778f4bae3552832e417efbf',
                                'size': 'b0412f81d58cda1e16f9ad11ad6469331b04b7d6e4586be5b34186b052f87103'}},
              {'slug': 'kask-vista-m',
               'category': 'helmets',
               'values': {'description_en': 'A helmet with an integrated visor that shields your eyes, as an alternative to separate '
                                            'goggles.\n'
                                            '\n'
                                            'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                            'comfort and makes cleaning easier. The integrated visor is made of polycarbonate. The Vista M '
                                            'variant is size M (55–59 cm). Head circumference: 55–59 cm; external dimensions: 27 × 23 × 24 '
                                            'cm. Weight: 620 g (one helmet with visor).',
                          'construction_en': 'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                             'comfort and makes cleaning easier. The integrated visor is made of polycarbonate.',
                          'dimensions_en': 'Head circumference: 55–59 cm; external dimensions: 27 × 23 × 24 cm.',
                          'weight_scope_en': 'one helmet with visor',
                          'size_en': 'M (55–59 cm)'},
               'fingerprints': {'description': '58f1ae94a11b05684691d47271f402bd1512bff15b7debeac3ee6a965290977b',
                                'construction': '8e56e3913e1ea50c87fb83886950f0b80155419dca2d78c543254c61b28ae5a5',
                                'dimensions': '181b7abd7405d91a12f83ca4f36473ae6a45e3998bba740d15f498020004f5c5',
                                'weight_scope': 'c8b2d2b2aaca4d7dbc2bbf211b39645fc0433f84fff8c7560416eb17ae30a0fa',
                                'size': 'b0412f81d58cda1e16f9ad11ad6469331b04b7d6e4586be5b34186b052f87103'}},
              {'slug': 'kask-district-m',
               'category': 'helmets',
               'values': {'description_en': 'A freestyle ski and snowboard helmet with a shape suited to snowpark riding.\n'
                                            '\n'
                                            'An ABS shell surrounds an EPS foam core. A removable polyester liner improves comfort and '
                                            'makes cleaning easier. The District M variant is size M (55–59 cm). Head circumference: 55–59 '
                                            'cm; external dimensions: 27 × 23 × 24 cm. Weight: 490 g (one helmet).',
                          'construction_en': 'An ABS shell surrounds an EPS foam core. A removable polyester liner improves comfort and '
                                             'makes cleaning easier.',
                          'dimensions_en': 'Head circumference: 55–59 cm; external dimensions: 27 × 23 × 24 cm.',
                          'weight_scope_en': 'one helmet',
                          'size_en': 'M (55–59 cm)'},
               'fingerprints': {'description': '75a705b4913e559d4b6db53b43a3ee7b8ee34fff9fa4db5b685f73f27ec87b62',
                                'construction': '92da1941a1ff30d23c9e6d4b5c2185b5f6a9899cfdfa71661502d63e69f51022',
                                'dimensions': '181b7abd7405d91a12f83ca4f36473ae6a45e3998bba740d15f498020004f5c5',
                                'weight_scope': '89c83308b6b470141aba383066e5afc33ee7e9108778f4bae3552832e417efbf',
                                'size': 'b0412f81d58cda1e16f9ad11ad6469331b04b7d6e4586be5b34186b052f87103'}},
              {'slug': 'gogle-halo-s3',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a darker lens for bright, sunny days on the slopes.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. A tinted lens for sunny days. The Halo S3 variant is size L. Frame '
                                            'width: 18 cm; frame height: 10 cm; adjustable strap. Weight: 150 g (goggles with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. A tinted lens for sunny days.',
                          'dimensions_en': 'Frame width: 18 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'L'},
               'fingerprints': {'description': '06be9df731db836ba2ee72602a787ed28f8da3fee27230a0176e85fc96ca0106',
                                'construction': '06d895834c7e8583a75112735196e4aa2594098ff4e43b0d596c0d41f486e980',
                                'dimensions': '0f2c47d6e8d08a03c6e55e9094d2d9a9da3365b462f7c3f89f2cea40d15ee353',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': '72dfcfb0c470ac255cde83fb8fe38de8a128188e03ea5ba5b2a93adbea1062fa'}},
              {'slug': 'gogle-mist-s1',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a lighter lens for overcast days and low-light conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. A lighter lens for overcast conditions. The Mist S1 variant is size '
                                            'L. Frame width: 18 cm; frame height: 10 cm; adjustable strap. Weight: 150 g (goggles with '
                                            'strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. A lighter lens for overcast conditions.',
                          'dimensions_en': 'Frame width: 18 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'L'},
               'fingerprints': {'description': 'fc0981a200bcf05c768a2bb75261b54c55f24256a7847ebf6f507933a6139c41',
                                'construction': '740b4123a9b6c3c07e27f51ad42c9c69dbdbf2a1e87a07a5b7fd9266910227f4',
                                'dimensions': '0f2c47d6e8d08a03c6e55e9094d2d9a9da3365b462f7c3f89f2cea40d15ee353',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': '72dfcfb0c470ac255cde83fb8fe38de8a128188e03ea5ba5b2a93adbea1062fa'}},
              {'slug': 'gogle-flux-ph',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a photochromic lens that adjusts its tint to changing light conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. The photochromic lens changes its tint with the light. The Flux PH '
                                            'variant is size L. Frame width: 18 cm; frame height: 10 cm; adjustable strap. Weight: 150 g '
                                            '(goggles with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. The photochromic lens changes its tint with the light.',
                          'dimensions_en': 'Frame width: 18 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'L'},
               'fingerprints': {'description': 'ac57cc311dd13986a07e1dd005dfb549be3fac4462f7e588d360797bfe9f4ab2',
                                'construction': 'cfc0af633f0e45620988a7cc58bf3f2f63ae2ef9c23d30cd98cb3c28a9f9a9b1',
                                'dimensions': '0f2c47d6e8d08a03c6e55e9094d2d9a9da3365b462f7c3f89f2cea40d15ee353',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': '72dfcfb0c470ac255cde83fb8fe38de8a128188e03ea5ba5b2a93adbea1062fa'}},
              {'slug': 'buty-snowboardowe-roam-500',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Versatile all-mountain snowboard boots for different riding styles and snow conditions.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Roam 500 variant is size EU 42. Outer '
                                            'sole length: 305 mm; cuff height: 30 cm. Weight: 1870 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 305 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 42'},
               'fingerprints': {'description': '249ba8ec3bcfcaf40215e8253f18af35c74a525d9b6eb6c0defbf7b2a06885c1',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': 'da2480650f2e8e732814b806e3ae8b78764f880bb2c0390dd5da61c707164c92',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '5d5489e7a0b03c14423eaa504450f93765902efba1d4ade1e25f00a6b04ca8f5'}},
              {'slug': 'buty-snowboardowe-flex-100',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Freestyle snowboard boots designed for freedom of movement during tricks and snowpark '
                                            'riding.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Flex 100 variant is size EU 40. Outer '
                                            'sole length: 295 mm; cuff height: 30 cm. Weight: 1750 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 295 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 40'},
               'fingerprints': {'description': '1d0002befef3f6c0da9c324e1118152e36476e6cc958ce5c5f8a03e2f2a15283',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': 'c4cdff475e75c809e7e983480146ecb89ac6d6cb496e3ee38cc79eab2112ebc2',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '22c7b2511a28f5323ed68fc98fd7080f884748069f781b44c362e3b3c5031e76'}},
              {'slug': 'buty-snowboardowe-rift-900',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Freeride snowboard boots with a supportive construction for precise control.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Rift 900 variant is size EU 43. Outer '
                                            'sole length: 310 mm; cuff height: 30 cm. Weight: 1930 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 310 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 43'},
               'fingerprints': {'description': 'cf9860499ad8e871c77290565100f19be560bdca5026339ce34fb278041086b8',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': '23992ab3a0ce7f719933923e03fcbfc15487f8bdba0ddd0ef86580a71469bd68',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '3cab36661199e9249070ebb869825f29ad3bcbfc04756ee14094e793ef48ee68'}},
              {'slug': 'buty-summit-27',
               'category': 'boots',
               'values': {'description_en': 'Alpine ski boots for recreational skiing on groomed slopes. Choose the correct Mondopoint '
                                            'size for your feet.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Summit 27 variant is size 27.0 MP. Mondopoint: 27.0 cm; długość podeszwy '
                                            'zewnętrznej: 310 mm; cuff height: 32 cm. Weight: 4060 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 27.0 cm; outer sole length: 310 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '27.0 MP'},
               'fingerprints': {'description': 'eedc57dbbffaa345bca77db066d28dd2b67e1e98c25c1fbf0b7c8e28311862f1',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': 'd07acd590f87468c60a22715454128d186f6600ea114789c6f37f997f80dbbb2',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '7b948a1e9b0a9b6e8cd14dc584c1be622b5ae1f4e1dd8e2cf3d5ec5e5e02e5aa'}},
              {'slug': 'buty-contour-100',
               'category': 'boots',
               'values': {'description_en': 'All-mountain ski boots for varied snow conditions and riding beyond groomed runs.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Contour 100 variant is size 26.0 MP. Mondopoint: 26.0 cm; długość '
                                            'podeszwy zewnętrznej: 300 mm; cuff height: 32 cm. Weight: 3980 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 26.0 cm; outer sole length: 300 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '26.0 MP'},
               'fingerprints': {'description': 'bef1b71be69cfabf6ed738ea47298d6081dcf4a9b53547e93328def36d262afd',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': 'acd4ace861dfa7f3c887e7642d9e7ef5f665102084a2025add5473073a6517e4',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '1681f4fde70d2c36a103a42575a16e39df29660f39ad9637fe90c279be05ff9b'}},
              {'slug': 'buty-cloud-80',
               'category': 'boots',
               'values': {'description_en': 'Alpine ski boots for recreational skiing on groomed slopes. Choose the correct Mondopoint '
                                            'size for your feet.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Cloud 80 variant is size 25.0 MP. Mondopoint: 25.0 cm; długość podeszwy '
                                            'zewnętrznej: 290 mm; cuff height: 32 cm. Weight: 3900 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 25.0 cm; outer sole length: 290 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '25.0 MP'},
               'fingerprints': {'description': '994e8ea31a65c4200953f165310b39adb63fc5c908a85d04ef4d008bc6293c55',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': '6bb8f8e3953635ad99ee3d9d63527fe6752cb72fb791e163e682efbd54c9a550',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '5c39789e29a633b3b83f94cc7b2e2fc4513208f75af55d6b89d9278c76d75bf5'}},
              {'slug': 'pokrowiec-trail-bag',
               'category': 'accessories',
               'values': {'description_en': 'A protective ski bag for travel and storage.\n'
                                            '\n'
                                            'Polyester fabric with a polyurethane coating, reinforced handles and a full-length zip. The '
                                            'bag holds a pair of skis with bindings. The Trail Bag variant is size Skis up to 190 cm. '
                                            'Length × width × height: 195 × 28 × 18 cm. Weight: 750 g (empty bag).',
                          'construction_en': 'Polyester fabric with a polyurethane coating, reinforced handles and a full-length zip. The '
                                             'bag holds a pair of skis with bindings.',
                          'dimensions_en': 'Length × width × height: 195 × 28 × 18 cm.',
                          'weight_scope_en': 'empty bag',
                          'size_en': 'Skis up to 190 cm'},
               'fingerprints': {'description': '5305914ad4de39a5f1adaa5a1b6ad70a5dc62159db7376960c1397cc7ef345c0',
                                'construction': 'de76d8e97235ddbc7af218aeea26340a7c50f7554b7ecd970a23003e593f9354',
                                'dimensions': 'f83cc2847b29c50aa95f1eeb86ec126315c140e527ada38d3f39b6d8ddf3c279',
                                'weight_scope': '7790ae794b5a00a53b620060b0961dbbda024c8f690dff949e1fce8bef1b5cd2',
                                'size': '9a7f000cdd435181b94d8011809043c7bb569d13694fb0422a9558e186d1c8a1'}},
              {'slug': 'plytka-axis-disc',
               'category': 'accessories',
               'values': {'description_en': 'A mounting disc and screws for compatible snowboard bindings.\n'
                                            '\n'
                                            'A polyamide mounting disc with four steel screws and washers. A set for mounting a compatible '
                                            'snowboard binding. The Axis Disc variant is size Disc 4 × 4. Disc diameter: 10 cm; mounting '
                                            'pattern: 4 × 4 cm; screw length: 16 mm. Weight: 140 g (disc with four screws).',
                          'construction_en': 'A polyamide mounting disc with four steel screws and washers. A set for mounting a '
                                             'compatible snowboard binding.',
                          'dimensions_en': 'Disc diameter: 10 cm; mounting pattern: 4 × 4 cm; screw length: 16 mm.',
                          'weight_scope_en': 'disc with four screws',
                          'size_en': 'Disc 4 × 4'},
               'fingerprints': {'description': '12fcdc14630e7c1b7313f338bcce711f566d9035b4f0a6eb900f244b11704643',
                                'construction': 'd80a9089b8bd0e738891c6c808b2d238feb24a7d619755fa5600e620797c4311',
                                'dimensions': '95b3ad8e254d2c6f4181e8154bf74c74083792fa0afb02f061f3c619ceb66111',
                                'weight_scope': '22bbf297cfd08886f2f0c213e0361783dd9f89439bd95249fe57b3099e414030',
                                'size': '4c9406ab93336e4a63ca5b2b6a3c954d8ff338b41d1ed1dda3429da5db880dce'}},
              {'slug': 'sruby-mount-kit',
               'category': 'accessories',
               'values': {'description_en': 'A spare screw and washer set for compatible snowboard bindings.\n'
                                            '\n'
                                            'Eight steel screws and washers for snowboard bindings. Match the thread and screw length to '
                                            'the inserts and binding base. The Mount Kit variant is size M6 × 16 mm. Thread: M6; screw '
                                            'length: 16 mm; washer diameter: 12 mm. Weight: 70 g (set of eight screws and washers).',
                          'construction_en': 'Eight steel screws and washers for snowboard bindings. Match the thread and screw length to '
                                             'the inserts and binding base.',
                          'dimensions_en': 'Thread: M6; screw length: 16 mm; washer diameter: 12 mm.',
                          'weight_scope_en': 'set of eight screws and washers',
                          'size_en': 'M6 × 16 mm'},
               'fingerprints': {'description': '70c7f158c24231f718c9a37169fb0a79e1a4456a4502965749a0728bc89b1c25',
                                'construction': 'f3bd9a6a6e5df67d735a91de850b2fc59441e9a13eb7db4b81edfebc9879044f',
                                'dimensions': '99722901881195734e996c958519585628e872311b446042ce54983aae879be6',
                                'weight_scope': '492007d473ce60d089d65e928f83d6a8086fbac0a9a02249262e069ba511aeb1',
                                'size': '6d98efa093017ed9c0fa2f0326ad36188ce98c53426860ddf8847702718c1a2b'}},
              {'slug': 'narty-alpine-178',
               'category': 'skis',
               'values': {'description_en': 'Piste skis with bindings for practising turns and spending a full day on groomed slopes.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Alpine 178 variant is size 178 cm. Length: 178 cm; sidecut tip / waist / tail: 124 '
                                            '/ 74 / 108 mm. Weight: 4180 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 178 cm; sidecut tip / waist / tail: 124 / 74 / 108 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '178 cm'},
               'fingerprints': {'description': '5cb5bda34e7d009db335f889412e2c0c96af6569cade11a4f2d89e780dd17a94',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': '327c24a4ffb9f7e0ee36466c654f0f117e1fb737b22a937b23b80bcb9098deb3',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'adbec4fafb440d368a2e03814c25c10312c191c9d19cec05f2b9b896044b8973'}},
              {'slug': 'narty-traverse-88',
               'category': 'skis',
               'values': {'description_en': 'Versatile all-mountain skis with bindings for piste runs and variable snow conditions.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Traverse 88 variant is size 180 cm. Length: 180 cm; sidecut tip / waist / tail: 130 '
                                            '/ 88 / 114 mm. Weight: 4200 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 180 cm; sidecut tip / waist / tail: 130 / 88 / 114 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '180 cm'},
               'fingerprints': {'description': 'f4f2d770d32146c88badff63846752d71c677f3b29775bc922c97dee968ebcba',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': 'eae23f03b2ccfe84f75441aa80f1017ed2c09a4d323a284e4da4af6fbc37bdf1',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': '36cc3d7049c6d40af5d955e61b5aa5f3db2ed89f405354e6a12d31c6d1a3bcff'}},
              {'slug': 'narty-ascend-95',
               'category': 'skis',
               'values': {'description_en': 'Touring skis with bindings and skins for climbing and skiing in mountain terrain.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. Carbon fibre stiffens the lightweight body. The Ascend 95 variant is size 171 cm. '
                                            'Length: 171 cm; sidecut tip / waist / tail: 126 / 95 / 113 mm. Weight: 3410 g (pair of skis '
                                            'with bindings and skins).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base. Carbon fibre stiffens the lightweight body.',
                          'dimensions_en': 'Length: 171 cm; sidecut tip / waist / tail: 126 / 95 / 113 mm.',
                          'weight_scope_en': 'pair of skis with bindings and skins',
                          'size_en': '171 cm'},
               'fingerprints': {'description': '3f42beaf1febcecf11cf855a4077b33ac1da5e256c52cb742b36bc6c027737c2',
                                'construction': '22c61e7c2af786a707fa399626fca9d320018cfb5721432569a2600b85b4faf2',
                                'dimensions': '7fee7c2586499cee5106265e20921742e6a9c188e033bce5fa8118d0f3715b4d',
                                'weight_scope': '9abdd8cfc3199d8f7222e01c293a936aa667b20a3bceb329fb1fec4f6b17738c',
                                'size': '7afe66b296e87665050a984eed52b0bc3a3ea5b58160fdc89b66f0529f80f9b1'}},
              {'slug': 'snowboard-drift-162',
               'category': 'snowboards',
               'values': {'description_en': 'An all-mountain snowboard for piste runs and exploring beyond the slopes. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Drift 162 variant is size 162 cm. Length: 162 cm; '
                                            'waist width: 26.1 cm. Weight: 3060 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 162 cm; waist width: 26.1 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '162 cm'},
               'fingerprints': {'description': '0f427639b065111ae6fdff90edeccf17c1078c1d76144ec72d5a18ebb821b109',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': 'f6b933e435d9faa3b519727a9053d9d766698dc2041e9387da1738190c5f9a50',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': 'a72050d716e864065f41a63b9d70d516a6612aa84a24c0ced430e26e6c36703a'}},
              {'slug': 'snowboard-orbit-156',
               'category': 'snowboards',
               'values': {'description_en': 'A freestyle snowboard for tricks, jumps and riding in the snowpark. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Orbit 156 variant is size 156 cm. Length: 156 cm; '
                                            'waist width: 25.2 cm. Weight: 2880 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 156 cm; waist width: 25.2 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '156 cm'},
               'fingerprints': {'description': '1438bbbbed865d26b15354d3f1a33dbb0869523c3814ed3269643637463d4820',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': '00afd9b3a1d59bce0081ac15b0e431f65969566858e1ec701cf8736efaef0470',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '9aeaebf33d572fe524cf8959a96c5ba5ce983ab1dd56913b4341d85c42ed86dc'}},
              {'slug': 'snowboard-glacier-163',
               'category': 'snowboards',
               'values': {'description_en': 'A freeride snowboard for soft snow and riding beyond groomed runs. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Glacier 163 variant is size 163 cm. Length: 163 cm; '
                                            'waist width: 26.1 cm. Weight: 3090 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 163 cm; waist width: 26.1 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '163 cm'},
               'fingerprints': {'description': 'b85f9285a0f6cdc168b43ba1a2622f8fa9f0babbfbb6c272ae5e7af60483a034',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': '821b8caf807bc8b74a115e5811180cb24d23bf9bffb835f0f8073f03da12054c',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '74830b33a4fe7947c1818e13f6106670fc3f10af6ff484c9b2dfb82fe48b62d4'}},
              {'slug': 'wiazania-latch-youth',
               'category': 'bindings',
               'values': {'description_en': 'Junior alpine ski bindings for piste skiing. Match the boot sole length and brake width to '
                                            'your equipment.\n'
                                            '\n'
                                            'A polyamide body, steel release mechanism and aluminium rail components. Toe and heel pieces '
                                            'form a set for a pair of skis. The Latch Youth variant is size Junior (sole 220–320 mm). Sole '
                                            'length range: 220–320 mm; brake width: 76 mm. Weight: 950 g (pair of bindings).',
                          'construction_en': 'A polyamide body, steel release mechanism and aluminium rail components. Toe and heel pieces '
                                             'form a set for a pair of skis.',
                          'dimensions_en': 'Sole length range: 220–320 mm; brake width: 76 mm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'Junior (sole 220–320 mm)'},
               'fingerprints': {'description': '2358d0eb10971657489f653e02a34c6b2348020955c043799fc1d5d30f964635',
                                'construction': 'd9b19017456d3dd402fade9b45451f31f7f5c28e8d68324b86d75ceff47ecd40',
                                'dimensions': '3278948259421393abd63f9e05813de70c8e47b5fe7306477ed68f0f3fc4ede2',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': '1f44e75681897db1ea279015d105fe3d5d7895bae39d258bcaf1d60494cada18'}},
              {'slug': 'wiazania-anchor-700',
               'category': 'bindings',
               'values': {'description_en': 'Strap snowboard bindings for all-mountain and freestyle riding. Choose the binding size to '
                                            'match your boots.\n'
                                            '\n'
                                            'A polyamide base and highback, aluminium buckles and cushioning EVA pads. Two straps hold the '
                                            'boot in the binding. The Anchor 700 variant is size L (EU 43–47). Base: 28 × 16 cm; highback '
                                            'height: 26 cm. Weight: 1900 g (pair of bindings).',
                          'construction_en': 'A polyamide base and highback, aluminium buckles and cushioning EVA pads. Two straps hold '
                                             'the boot in the binding.',
                          'dimensions_en': 'Base: 28 × 16 cm; highback height: 26 cm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'L (EU 43–47)'},
               'fingerprints': {'description': '08b0bc566714862ac514dba2c8f0c337df723733694a606d595a82de6e0e2c6e',
                                'construction': '657bf4bb7840aff8839570e6044c3afc9390d59eda4b016a236d6fa365114d54',
                                'dimensions': '390e1593d088bdb101f8ec61f56d97afa2b252b488330294dc9e78aec2197282',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': '2a21ee5cb87acd25f777a9d4f449f3254cf969e19000a9ba6ff09ff97368ae76'}},
              {'slug': 'wiazania-swift-400',
               'category': 'bindings',
               'values': {'description_en': 'Quick-entry snowboard bindings with a rear-opening highback for easier boot entry.\n'
                                            '\n'
                                            'A polyamide base and highback, aluminium buckles and cushioning EVA pads. A rear-opening '
                                            'highback makes boot entry easier. The Swift 400 variant is size L (EU 43–47). Base: 28 × 16 '
                                            'cm; highback height: 26 cm. Weight: 1900 g (pair of bindings).',
                          'construction_en': 'A polyamide base and highback, aluminium buckles and cushioning EVA pads. A rear-opening '
                                             'highback makes boot entry easier.',
                          'dimensions_en': 'Base: 28 × 16 cm; highback height: 26 cm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'L (EU 43–47)'},
               'fingerprints': {'description': 'b88b5c02f7b7045ae69917170b3a4d030df25193ea2722eaf5622799f4fbe2be',
                                'construction': 'abbb2c53e13fef07cc155446801ea109e81161fd619095bb441740fc8b30b2df',
                                'dimensions': '390e1593d088bdb101f8ec61f56d97afa2b252b488330294dc9e78aec2197282',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': '2a21ee5cb87acd25f777a9d4f449f3254cf969e19000a9ba6ff09ff97368ae76'}},
              {'slug': 'kask-ridge-l',
               'category': 'helmets',
               'values': {'description_en': 'A classic helmet for recreational skiing and snowboarding. Choose the size to match your head '
                                            'circumference.\n'
                                            '\n'
                                            'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                            'comfort and makes cleaning easier. The Ridge L variant is size L (59–62 cm). Head '
                                            'circumference: 59–62 cm; external dimensions: 28 × 24 × 25 cm. Weight: 480 g (one helmet).',
                          'construction_en': 'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                             'comfort and makes cleaning easier.',
                          'dimensions_en': 'Head circumference: 59–62 cm; external dimensions: 28 × 24 × 25 cm.',
                          'weight_scope_en': 'one helmet',
                          'size_en': 'L (59–62 cm)'},
               'fingerprints': {'description': '632871db494689bee4f68cfd0be3d372ea727d3c228319e2d66ca618f866a186',
                                'construction': 'bc95272f515ae039ff3d1ec028a2e914fc51c91aebd56a789d657004fc9d35ae',
                                'dimensions': '974b89fac070e0dfca94778ae618ef8faeea48dd69b02b18e070c2c9f3eb6152',
                                'weight_scope': '89c83308b6b470141aba383066e5afc33ee7e9108778f4bae3552832e417efbf',
                                'size': 'eec9a1d2138b7c80e440eae4dc64d1c8329db053509c69c20c2f0960d462904f'}},
              {'slug': 'kask-vista-l',
               'category': 'helmets',
               'values': {'description_en': 'A helmet with an integrated visor that shields your eyes, as an alternative to separate '
                                            'goggles.\n'
                                            '\n'
                                            'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                            'comfort and makes cleaning easier. The integrated visor is made of polycarbonate. The Vista L '
                                            'variant is size L (59–62 cm). Head circumference: 59–62 cm; external dimensions: 28 × 24 × 25 '
                                            'cm. Weight: 650 g (one helmet with visor).',
                          'construction_en': 'A polycarbonate shell surrounds an EPS foam core. A removable polyester liner improves '
                                             'comfort and makes cleaning easier. The integrated visor is made of polycarbonate.',
                          'dimensions_en': 'Head circumference: 59–62 cm; external dimensions: 28 × 24 × 25 cm.',
                          'weight_scope_en': 'one helmet with visor',
                          'size_en': 'L (59–62 cm)'},
               'fingerprints': {'description': 'b7182a846d93ff86680560ff04311a7a1ec228fa96724a9dabb995f5cabf7d87',
                                'construction': '8e56e3913e1ea50c87fb83886950f0b80155419dca2d78c543254c61b28ae5a5',
                                'dimensions': '974b89fac070e0dfca94778ae618ef8faeea48dd69b02b18e070c2c9f3eb6152',
                                'weight_scope': 'c8b2d2b2aaca4d7dbc2bbf211b39645fc0433f84fff8c7560416eb17ae30a0fa',
                                'size': 'eec9a1d2138b7c80e440eae4dc64d1c8329db053509c69c20c2f0960d462904f'}},
              {'slug': 'kask-district-l',
               'category': 'helmets',
               'values': {'description_en': 'A freestyle ski and snowboard helmet with a shape suited to snowpark riding.\n'
                                            '\n'
                                            'An ABS shell surrounds an EPS foam core. A removable polyester liner improves comfort and '
                                            'makes cleaning easier. The District L variant is size L (59–62 cm). Head circumference: 59–62 '
                                            'cm; external dimensions: 28 × 24 × 25 cm. Weight: 520 g (one helmet).',
                          'construction_en': 'An ABS shell surrounds an EPS foam core. A removable polyester liner improves comfort and '
                                             'makes cleaning easier.',
                          'dimensions_en': 'Head circumference: 59–62 cm; external dimensions: 28 × 24 × 25 cm.',
                          'weight_scope_en': 'one helmet',
                          'size_en': 'L (59–62 cm)'},
               'fingerprints': {'description': 'df08955f5de4e02b8f6e9d925733d93437812ae5b96bec48ca020cffffa2e549',
                                'construction': '92da1941a1ff30d23c9e6d4b5c2185b5f6a9899cfdfa71661502d63e69f51022',
                                'dimensions': '974b89fac070e0dfca94778ae618ef8faeea48dd69b02b18e070c2c9f3eb6152',
                                'weight_scope': '89c83308b6b470141aba383066e5afc33ee7e9108778f4bae3552832e417efbf',
                                'size': 'eec9a1d2138b7c80e440eae4dc64d1c8329db053509c69c20c2f0960d462904f'}},
              {'slug': 'gogle-halo-wide',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a darker lens for bright, sunny days on the slopes.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. A tinted lens for sunny days. The Halo Wide variant is size XL. Frame '
                                            'width: 19 cm; frame height: 10 cm; adjustable strap. Weight: 165 g (goggles with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. A tinted lens for sunny days.',
                          'dimensions_en': 'Frame width: 19 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'XL'},
               'fingerprints': {'description': '2874ecfe82997cb67e267ea3cd6403b786713336d6c226080ea7694e2b3906e4',
                                'construction': '06d895834c7e8583a75112735196e4aa2594098ff4e43b0d596c0d41f486e980',
                                'dimensions': 'ea5e4bfeba18fb8d25e7ef8220c868ab5c83e9c1e363d4ae200502389c0dc43c',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': 'f365705bb0612eed918b30a166bd7b5d48908d58cbfb7da0deff2a7b953199ce'}},
              {'slug': 'gogle-mist-wide',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a lighter lens for overcast days and low-light conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. A lighter lens for overcast conditions. The Mist Wide variant is size '
                                            'XL. Frame width: 19 cm; frame height: 10 cm; adjustable strap. Weight: 165 g (goggles with '
                                            'strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. A lighter lens for overcast conditions.',
                          'dimensions_en': 'Frame width: 19 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'XL'},
               'fingerprints': {'description': '15804c1f360fd69777413dd0ae2bb0982b249c9107c76127f812288f3f4dd310',
                                'construction': '740b4123a9b6c3c07e27f51ad42c9c69dbdbf2a1e87a07a5b7fd9266910227f4',
                                'dimensions': 'ea5e4bfeba18fb8d25e7ef8220c868ab5c83e9c1e363d4ae200502389c0dc43c',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': 'f365705bb0612eed918b30a166bd7b5d48908d58cbfb7da0deff2a7b953199ce'}},
              {'slug': 'gogle-flux-pro',
               'category': 'goggles',
               'values': {'description_en': 'Goggles with a photochromic lens that adjusts its tint to changing light conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. The photochromic lens changes its tint with the light. The Flux Pro '
                                            'variant is size L. Frame width: 18 cm; frame height: 10 cm; adjustable strap. Weight: 150 g '
                                            '(goggles with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. The photochromic lens changes its tint with the light.',
                          'dimensions_en': 'Frame width: 18 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'L'},
               'fingerprints': {'description': '171eb0b12fbcc0ecb731c3298ae46f582e08fdf51e791e2f79dabd4f1d286aea',
                                'construction': 'cfc0af633f0e45620988a7cc58bf3f2f63ae2ef9c23d30cd98cb3c28a9f9a9b1',
                                'dimensions': '0f2c47d6e8d08a03c6e55e9094d2d9a9da3365b462f7c3f89f2cea40d15ee353',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': '72dfcfb0c470ac255cde83fb8fe38de8a128188e03ea5ba5b2a93adbea1062fa'}},
              {'slug': 'buty-snowboardowe-roam-700',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Versatile all-mountain snowboard boots for different riding styles and snow conditions.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Roam 700 variant is size EU 43. Outer '
                                            'sole length: 310 mm; cuff height: 30 cm. Weight: 1930 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 310 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 43'},
               'fingerprints': {'description': '821926caa5140d142f84ea5b06fe563ddbe354f87bfe33eee6673f8f7b10b1ea',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': '23992ab3a0ce7f719933923e03fcbfc15487f8bdba0ddd0ef86580a71469bd68',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '3cab36661199e9249070ebb869825f29ad3bcbfc04756ee14094e793ef48ee68'}},
              {'slug': 'buty-snowboardowe-flex-200',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Freestyle snowboard boots designed for freedom of movement during tricks and snowpark '
                                            'riding.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Flex 200 variant is size EU 41. Outer '
                                            'sole length: 300 mm; cuff height: 30 cm. Weight: 1810 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 300 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 41'},
               'fingerprints': {'description': '881bd2c4fcc5920366144024056ba36a00ec06d3175a9932e088bbc8ae947585',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': '6b348b5bec94608941400f78f5b95e7194cb1f501274f3b68353b76cf62b0560',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '38ff32465462924b1d29313252c94d62c0acb33461d3c4bddcb446181e81b8b1'}},
              {'slug': 'buty-snowboardowe-rift-950',
               'category': 'snowboard_boots',
               'values': {'description_en': 'Freeride snowboard boots with a supportive construction for precise control.\n'
                                            '\n'
                                            'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                            'outsole. Soft padding surrounds the foot and ankle. The Rift 950 variant is size EU 44. Outer '
                                            'sole length: 315 mm; cuff height: 30 cm. Weight: 1990 g (pair of boots).',
                          'construction_en': 'A polyester upper reinforced with polyurethane, an inner liner with EVA foam and a rubber '
                                             'outsole. Soft padding surrounds the foot and ankle.',
                          'dimensions_en': 'Outer sole length: 315 mm; cuff height: 30 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': 'EU 44'},
               'fingerprints': {'description': '27b99b93e2f10bfa35365c7a6847bd222c45f2186720370fad710aca4a6fff56',
                                'construction': '36449849d3ba0413b9feb28473b47da7550bfe1b9dc1898c65ea3ea947130fbb',
                                'dimensions': '60fb024d55ef90614f023d99fa11c084706e26cfcef16bb35a5f0211b93f86e7',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': 'a588fc2287f53e025b774145052731f62cd5f741a1ac0bf5804fbedfd4f511bd'}},
              {'slug': 'buty-contour-110',
               'category': 'boots',
               'values': {'description_en': 'All-mountain ski boots for varied snow conditions and riding beyond groomed runs.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Contour 110 variant is size 28.0 MP. Mondopoint: 28.0 cm; długość '
                                            'podeszwy zewnętrznej: 320 mm; cuff height: 32 cm. Weight: 4140 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 28.0 cm; outer sole length: 320 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '28.0 MP'},
               'fingerprints': {'description': '6a6998e929a8c72e8dbbbb9764f6d9f18ddc38b2ecd7e49ba23282a9981ce585',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': '5551162cf898ee49acad105becbac4cfb46a0c96367cf868cf605fd09377b197',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '7f8c57175e76c53d83cca52fced0801e9e17418c46d3217efc6505d3bd2daea8'}},
              {'slug': 'narty-powder-108',
               'category': 'skis',
               'values': {'description_en': 'Freeride skis with bindings for soft snow and skiing beyond groomed runs.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Powder 108 variant is size 181 cm. Length: 181 cm; sidecut tip / waist / tail: 140 '
                                            '/ 108 / 129 mm. Weight: 4510 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 181 cm; sidecut tip / waist / tail: 140 / 108 / 129 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '181 cm'},
               'fingerprints': {'description': '07a35c74a4da44fa1dab6b5d0dc1bb86d8c7f21774726f8aeb291c7b40e2d9a8',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': '55154c17f248ab319e688bad5edbdc56a65ddd25f9d543e4ac15b10b5a6f50f2',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': '86d75c957704da9924d0a8b938cb66ffbd15aa01c0987cb813a0c46aed0f395b'}},
              {'slug': 'narty-powder-114',
               'category': 'skis',
               'values': {'description_en': 'Freeride skis with bindings for soft snow and skiing beyond groomed runs.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Powder 114 variant is size 188 cm. Length: 188 cm; sidecut tip / waist / tail: 146 '
                                            '/ 114 / 135 mm. Weight: 4580 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 188 cm; sidecut tip / waist / tail: 146 / 114 / 135 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '188 cm'},
               'fingerprints': {'description': 'ea16cb28dd5bfffba9ebfe3df7ede9b61edae601c79512dbefc3ae28caf8dc3c',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': 'fee75910625dcbe4c8f5815d25d6f849d21e1a3f01d65698eb2a5a5a52f839b0',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'b50ddddb04805d3df1681590aeb609d4d21a80f9b21087a0859d479f2979a802'}},
              {'slug': 'narty-pulse-164',
               'category': 'skis',
               'values': {'description_en': 'Twin-tip skis with bindings for freestyle riding and playing in the snow.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Pulse 164 variant is size 164 cm. Length: 164 cm; sidecut tip / waist / tail: 118 / '
                                            '88 / 112 mm. Weight: 3840 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 164 cm; sidecut tip / waist / tail: 118 / 88 / 112 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '164 cm'},
               'fingerprints': {'description': '6208c1a9c1cdfae1db8712513d2f9b24c1269b4908161d161402626a839273ef',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': '11da4aec4f2e52387f729c279a3bb59e7e1eda88c352739276ef6529f30b0098',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': '3292538bd0c56b49c9ad08bbdf0bbbcf9c392a7fc1b9eab0153723716a318093'}},
              {'slug': 'narty-pulse-172',
               'category': 'skis',
               'values': {'description_en': 'Twin-tip skis with bindings for freestyle riding and playing in the snow.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Pulse 172 variant is size 172 cm. Length: 172 cm; sidecut tip / waist / tail: 120 / '
                                            '90 / 114 mm. Weight: 3820 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 172 cm; sidecut tip / waist / tail: 120 / 90 / 114 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '172 cm'},
               'fingerprints': {'description': '5222a6dd2cb5612165e544867266398a0027522444329edc14dbeaddf93fc458',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': 'fe77a9d2fad2dd238629e4302ff98b8e2c6efed177a06e2b8ce9d1eec181f0fb',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'd963cf0ec1f39b8c3486f44c5dc4add576437a67370992de5de33d90dc425f72'}},
              {'slug': 'narty-nordic-180',
               'category': 'skis',
               'values': {'description_en': 'Cross-country skis with bindings for skating technique on prepared trails.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. The Nordic 180 variant is '
                                            'size 180 cm. Length: 180 cm; sidecut tip / waist / tail: 44 / 44 / 44 mm. Weight: 1350 g '
                                            '(pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base.',
                          'dimensions_en': 'Length: 180 cm; sidecut tip / waist / tail: 44 / 44 / 44 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '180 cm'},
               'fingerprints': {'description': '5667a18a9bc9725461808079c4c3ee3f315cc7472b4720e1ca2d61675bf4c7e1',
                                'construction': 'd9b1c43e75132040c62c1bc8d2bfd3b161cd65e65be27522f8e4a44544503564',
                                'dimensions': '3cb5cf0d141a696fb2ff9b22da5dd5fc7427ecf219f3e47ca8fe8972e42815c8',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': '36cc3d7049c6d40af5d955e61b5aa5f3db2ed89f405354e6a12d31c6d1a3bcff'}},
              {'slug': 'narty-nordic-190',
               'category': 'skis',
               'values': {'description_en': 'Cross-country skis with bindings for skating technique on prepared trails.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. The Nordic 190 variant is '
                                            'size 190 cm. Length: 190 cm; sidecut tip / waist / tail: 44 / 44 / 44 mm. Weight: 1350 g '
                                            '(pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base.',
                          'dimensions_en': 'Length: 190 cm; sidecut tip / waist / tail: 44 / 44 / 44 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '190 cm'},
               'fingerprints': {'description': 'b044d8f0ccafd4c648f9fe909968b89f68983754599dff68260e344daf5296f8',
                                'construction': 'd9b1c43e75132040c62c1bc8d2bfd3b161cd65e65be27522f8e4a44544503564',
                                'dimensions': 'ea4fd55af059d3597eb316be80ba45a7a3cb6c9bd12672facfeb3a15265799ec',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'a6e84ee3e279e2dadb1d24dbd7ce175270754fa0b1492a5bb8c43f0930584f15'}},
              {'slug': 'narty-velocity-165',
               'category': 'skis',
               'values': {'description_en': 'Sporty slalom skis with bindings for dynamic turns on groomed slopes. Designed for advanced '
                                            'skiers.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Velocity 165 variant is size 165 cm. Length: 165 cm; sidecut tip / waist / tail: '
                                            '121 / 68 / 104 mm. Weight: 4750 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 165 cm; sidecut tip / waist / tail: 121 / 68 / 104 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '165 cm'},
               'fingerprints': {'description': '7d15f5043bd7529680b3bf7cae6c79ef58d76a8cb3cb55f0230f3c2662ded676',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': 'd8c812907c331c097ea7d09f119e28ffcb44cd3cf89d3e8eddade664040b126c',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': '5db53905f54b5d63b7d618f098d5e7bdab412b22aafd1a10effa241912c21ba6'}},
              {'slug': 'narty-velocity-170',
               'category': 'skis',
               'values': {'description_en': 'Sporty slalom skis with bindings for dynamic turns on groomed slopes. Designed for advanced '
                                            'skiers.\n'
                                            '\n'
                                            'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                            'base. The Velocity 170 variant is size 170 cm. Length: 170 cm; sidecut tip / waist / tail: '
                                            '123 / 69 / 105 mm. Weight: 4700 g (pair of skis with bindings).',
                          'construction_en': 'A wooden core reinforced with fibreglass and a polyethylene base. Steel edges run along the '
                                             'base.',
                          'dimensions_en': 'Length: 170 cm; sidecut tip / waist / tail: 123 / 69 / 105 mm.',
                          'weight_scope_en': 'pair of skis with bindings',
                          'size_en': '170 cm'},
               'fingerprints': {'description': '268cdd8d6f0a35379602c7f38b5dc17f8616d09cf086752e465a2b65e59afe4a',
                                'construction': '7b12f5c3df751f727681a3d2c6ddc0e9ad70d2a5cb2d35f9639ee03c4e016269',
                                'dimensions': 'fa777eba7e4ad80cb21886242c228976035b77d9b959619c84df267c457400e8',
                                'weight_scope': '503c02779f2b18e41dcd6dd185063a842de718ab1b110f65abc6d96b4f91e0bd',
                                'size': 'd74b86551b5d6718b3b8a66fbdc4ecd48b2dcfd33cdc28562b3131de664b9f03'}},
              {'slug': 'snowboard-edge-156',
               'category': 'snowboards',
               'values': {'description_en': 'A snowboard for piste riding and controlled carving turns on the edges. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Edge 156 variant is size 156 cm. Length: 156 cm; '
                                            'waist width: 25.2 cm. Weight: 2880 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 156 cm; waist width: 25.2 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '156 cm'},
               'fingerprints': {'description': '94259b180fa785eda59051ec3804180b4f010eb39e5f0faca766133c1819a7ed',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': '00afd9b3a1d59bce0081ac15b0e431f65969566858e1ec701cf8736efaef0470',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': '9aeaebf33d572fe524cf8959a96c5ba5ce983ab1dd56913b4341d85c42ed86dc'}},
              {'slug': 'snowboard-edge-162',
               'category': 'snowboards',
               'values': {'description_en': 'A snowboard for piste riding and controlled carving turns on the edges. Bindings are sold '
                                            'separately.\n'
                                            '\n'
                                            'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                            'protects the laminate from moisture. The Edge 162 variant is size 162 cm. Length: 162 cm; '
                                            'waist width: 26.1 cm. Weight: 3060 g (board without bindings).',
                          'construction_en': 'A wooden core laminated with fibreglass, a polyethylene base and steel edges. The top sheet '
                                             'protects the laminate from moisture.',
                          'dimensions_en': 'Length: 162 cm; waist width: 26.1 cm.',
                          'weight_scope_en': 'board without bindings',
                          'size_en': '162 cm'},
               'fingerprints': {'description': '308ee916cd9b8e2c3b39238ca66a7450494dbb7e05482d5a2db796aeabc9ea94',
                                'construction': '6cfd4bc9cc2f488ccd5bf5c4e196eeacf05dafd74236a4f4f10804505754c2b3',
                                'dimensions': 'f6b933e435d9faa3b519727a9053d9d766698dc2041e9387da1738190c5f9a50',
                                'weight_scope': 'f7f07ce7708b43f2746997cf47a04e51ffc0c3fb061b73440ede7dc97cfaf8b3',
                                'size': 'a72050d716e864065f41a63b9d70d516a6612aa84a24c0ced430e26e6c36703a'}},
              {'slug': 'wiazania-ascent-10',
               'category': 'bindings',
               'values': {'description_en': 'Pin touring bindings with uphill and downhill modes. Compatible touring boots are required.\n'
                                            '\n'
                                            'An aluminium body with steel pins and polyamide pads. The movable heel piece switches between '
                                            'uphill and downhill modes. The Ascent 10 variant is size Sole 260–310 mm. Sole range: 260–310 '
                                            'mm; heel adjustment: 30 mm. Weight: 650 g (pair of bindings).',
                          'construction_en': 'An aluminium body with steel pins and polyamide pads. The movable heel piece switches '
                                             'between uphill and downhill modes.',
                          'dimensions_en': 'Sole range: 260–310 mm; heel adjustment: 30 mm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'Sole 260–310 mm'},
               'fingerprints': {'description': '986c7c513f7a7691a1527a9e90e1def6f168780c163c2f7a53a67559ffeb6d75',
                                'construction': '702f1e36e2885948e7711a7ff55bb99dc41c2171ca3eb8a623fcf9ed7b220915',
                                'dimensions': '3f600fc5aee5c1320f61676b3b2b5318e62927ef57863502883ed3acb2bb21ef',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': 'df9f25136e39a89b78c349640ee23df6d198d4867478f0dbc7ffc5347093cb48'}},
              {'slug': 'wiazania-ascent-12',
               'category': 'bindings',
               'values': {'description_en': 'Pin touring bindings with uphill and downhill modes. Compatible touring boots are required.\n'
                                            '\n'
                                            'An aluminium body with steel pins and polyamide pads. The movable heel piece switches between '
                                            'uphill and downhill modes. The Ascent 12 variant is size Sole 280–330 mm. Sole range: 280–330 '
                                            'mm; heel adjustment: 30 mm. Weight: 690 g (pair of bindings).',
                          'construction_en': 'An aluminium body with steel pins and polyamide pads. The movable heel piece switches '
                                             'between uphill and downhill modes.',
                          'dimensions_en': 'Sole range: 280–330 mm; heel adjustment: 30 mm.',
                          'weight_scope_en': 'pair of bindings',
                          'size_en': 'Sole 280–330 mm'},
               'fingerprints': {'description': '1ae90aeb7457346be836400f3b1820fbf84d35941f4f4b87e4ff70b5423cafb8',
                                'construction': '702f1e36e2885948e7711a7ff55bb99dc41c2171ca3eb8a623fcf9ed7b220915',
                                'dimensions': 'd9896e61b5717fd376616bb25377e5e432d6d2d02a5fb074d8dae5bd6648cb39',
                                'weight_scope': '042ddfe8e7b2ea56ea86dba51c8e47f883dfb76b64d02cc812fed6a8db68faa2',
                                'size': '43d296de09125f8c4d342b187da400cfeae9f5de9b4758a390a5b672af8f2330'}},
              {'slug': 'buty-climb-27',
               'category': 'boots',
               'values': {'description_en': 'Touring ski boots with a movable cuff for climbing and a locking mode for downhill skiing. '
                                            'Use compatible touring bindings.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. A movable polyamide cuff has an uphill mode, while the sole has rubber '
                                            'sections. The Climb 27 variant is size 27.0 MP. Mondopoint: 27.0 cm; długość podeszwy '
                                            'zewnętrznej: 310 mm; cuff height: 32 cm. Weight: 2760 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot. A movable polyamide cuff has an uphill mode, while the sole has rubber '
                                             'sections.',
                          'dimensions_en': 'Mondopoint: 27.0 cm; outer sole length: 310 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '27.0 MP'},
               'fingerprints': {'description': '3ee26374306a67cd3be47612bd4baa842837e9282c5a6aeb044737bca5de9c59',
                                'construction': '85550b363edae3d6d042381ea4fa0b5a5a6ef4a5b9acbe8d05bf55765d5f6107',
                                'dimensions': 'd07acd590f87468c60a22715454128d186f6600ea114789c6f37f997f80dbbb2',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '7b948a1e9b0a9b6e8cd14dc584c1be622b5ae1f4e1dd8e2cf3d5ec5e5e02e5aa'}},
              {'slug': 'buty-climb-28',
               'category': 'boots',
               'values': {'description_en': 'Touring ski boots with a movable cuff for climbing and a locking mode for downhill skiing. '
                                            'Use compatible touring bindings.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. A movable polyamide cuff has an uphill mode, while the sole has rubber '
                                            'sections. The Climb 28 variant is size 28.0 MP. Mondopoint: 28.0 cm; długość podeszwy '
                                            'zewnętrznej: 320 mm; cuff height: 32 cm. Weight: 2840 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot. A movable polyamide cuff has an uphill mode, while the sole has rubber '
                                             'sections.',
                          'dimensions_en': 'Mondopoint: 28.0 cm; outer sole length: 320 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '28.0 MP'},
               'fingerprints': {'description': '11faf874869a3d746f57515467893f6ac94d6693677160521bf06a914ae5d16b',
                                'construction': '85550b363edae3d6d042381ea4fa0b5a5a6ef4a5b9acbe8d05bf55765d5f6107',
                                'dimensions': '5551162cf898ee49acad105becbac4cfb46a0c96367cf868cf605fd09377b197',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '7f8c57175e76c53d83cca52fced0801e9e17418c46d3217efc6505d3bd2daea8'}},
              {'slug': 'buty-race-pro-26',
               'category': 'boots',
               'values': {'description_en': 'Sporty ski boots for precise piste skiing. A stiff construction for advanced skiers.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Race Pro 26 variant is size 26.0 MP. Mondopoint: 26.0 cm; długość '
                                            'podeszwy zewnętrznej: 300 mm; cuff height: 32 cm. Weight: 3980 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 26.0 cm; outer sole length: 300 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '26.0 MP'},
               'fingerprints': {'description': '969be84899fb7afb9ebca76adb0aa973531fe1c2edc38b59e321c79e7cb06b03',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': 'acd4ace861dfa7f3c887e7642d9e7ef5f665102084a2025add5473073a6517e4',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '1681f4fde70d2c36a103a42575a16e39df29660f39ad9637fe90c279be05ff9b'}},
              {'slug': 'buty-race-pro-27',
               'category': 'boots',
               'values': {'description_en': 'Sporty ski boots for precise piste skiing. A stiff construction for advanced skiers.\n'
                                            '\n'
                                            'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                            'secure the foot. The Race Pro 27 variant is size 27.0 MP. Mondopoint: 27.0 cm; długość '
                                            'podeszwy zewnętrznej: 310 mm; cuff height: 32 cm. Weight: 4060 g (pair of boots).',
                          'construction_en': 'A polyurethane shell, aluminium buckles and a polyester inner liner. Adjustable buckles help '
                                             'secure the foot.',
                          'dimensions_en': 'Mondopoint: 27.0 cm; outer sole length: 310 mm; cuff height: 32 cm.',
                          'weight_scope_en': 'pair of boots',
                          'size_en': '27.0 MP'},
               'fingerprints': {'description': '10674ff05087da6f6fda39a3305b2beb2617654c19585e00cc4ce07e7d1f3abc',
                                'construction': '811821e74cf974abdda1d0b3cf67516a12298c69a2ae66fd35e107e15e1e2ead',
                                'dimensions': 'd07acd590f87468c60a22715454128d186f6600ea114789c6f37f997f80dbbb2',
                                'weight_scope': '8c7fb3eff6e8d8d6827d46b9dda30fb8cafff10044aff9a8330180734fdba913',
                                'size': '7b948a1e9b0a9b6e8cd14dc584c1be622b5ae1f4e1dd8e2cf3d5ec5e5e02e5aa'}},
              {'slug': 'gogle-clear-otg',
               'category': 'goggles',
               'values': {'description_en': 'Over-the-glasses goggles with space for prescription glasses and a darker lens for sunny '
                                            'conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. The frame has room for prescription glasses. The Clear OTG variant is '
                                            'size L. Frame width: 18 cm; frame height: 10 cm; adjustable strap. Weight: 150 g (goggles '
                                            'with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. The frame has room for prescription glasses.',
                          'dimensions_en': 'Frame width: 18 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'L'},
               'fingerprints': {'description': '5532ffbabe5ec08584fa5555609cc78fd60d07ceee1348e3e3b58da7f29ae73d',
                                'construction': '1d24db204d5271243308f26c85946cfeebad5f057203865ab4f2580a83ce6eb1',
                                'dimensions': '0f2c47d6e8d08a03c6e55e9094d2d9a9da3365b462f7c3f89f2cea40d15ee353',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': '72dfcfb0c470ac255cde83fb8fe38de8a128188e03ea5ba5b2a93adbea1062fa'}},
              {'slug': 'gogle-clear-otg-wide',
               'category': 'goggles',
               'values': {'description_en': 'Over-the-glasses goggles with space for prescription glasses and a darker lens for sunny '
                                            'conditions.\n'
                                            '\n'
                                            'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                            'silicone grip sections. The frame has room for prescription glasses. The Clear OTG Wide '
                                            'variant is size XL. Frame width: 19 cm; frame height: 10 cm; adjustable strap. Weight: 165 g '
                                            '(goggles with strap).',
                          'construction_en': 'A polycarbonate lens in a flexible polyurethane frame. The adjustable polyester strap has '
                                             'silicone grip sections. The frame has room for prescription glasses.',
                          'dimensions_en': 'Frame width: 19 cm; frame height: 10 cm; adjustable strap.',
                          'weight_scope_en': 'goggles with strap',
                          'size_en': 'XL'},
               'fingerprints': {'description': '0dadd5dcf14da302796a321a0dd1fcc3bd51296f5c1e0c7dad06c3a8ba6e4641',
                                'construction': '1d24db204d5271243308f26c85946cfeebad5f057203865ab4f2580a83ce6eb1',
                                'dimensions': 'ea5e4bfeba18fb8d25e7ef8220c868ab5c83e9c1e363d4ae200502389c0dc43c',
                                'weight_scope': 'fc8bb8ae7571f09e9bca2b5d83d14da069c589b173d12eddecc7e2774d03f898',
                                'size': 'f365705bb0612eed918b30a166bd7b5d48908d58cbfb7da0deff2a7b953199ce'}}],
 'materials': [{'code': 'wood', 'name': 'Drewno', 'name_en': 'Wood'},
               {'code': 'fiberglass', 'name': 'Włókno szklane', 'name_en': 'Fibreglass'},
               {'code': 'carbon', 'name': 'Włókno węglowe', 'name_en': 'Carbon fibre'},
               {'code': 'steel', 'name': 'Stal', 'name_en': 'Steel'},
               {'code': 'aluminium', 'name': 'Aluminium', 'name_en': 'Aluminium'},
               {'code': 'polyethylene', 'name': 'Polietylen (PE)', 'name_en': 'Polyethylene (PE)'},
               {'code': 'polyamide', 'name': 'Poliamid (PA)', 'name_en': 'Polyamide (PA)'},
               {'code': 'polyurethane', 'name': 'Poliuretan (PU)', 'name_en': 'Polyurethane (PU)'},
               {'code': 'polycarbonate', 'name': 'Poliwęglan (PC)', 'name_en': 'Polycarbonate (PC)'},
               {'code': 'abs', 'name': 'Tworzywo ABS', 'name_en': 'ABS plastic'},
               {'code': 'eps', 'name': 'Pianka EPS', 'name_en': 'EPS foam'},
               {'code': 'eva', 'name': 'Pianka EVA', 'name_en': 'EVA foam'},
               {'code': 'polyester', 'name': 'Poliester', 'name_en': 'Polyester'},
               {'code': 'rubber', 'name': 'Guma', 'name_en': 'Rubber'},
               {'code': 'silicone', 'name': 'Silikon', 'name_en': 'Silicone'}]}


def populate_english(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    Material = apps.get_model("catalog", "Material")
    alias = schema_editor.connection.alias
    for entry in DATA["products"]:
        product = Product.objects.using(alias).filter(slug=entry["slug"], category=entry["category"]).first()
        if product is None:
            continue
        changes = {}
        for field, fingerprint in entry["fingerprints"].items():
            if hashlib.sha256(getattr(product, field).encode()).hexdigest() == fingerprint:
                english_field = field + "_en"
                if not getattr(product, english_field):
                    changes[english_field] = entry["values"][english_field]
        if changes:
            Product.objects.using(alias).filter(pk=product.pk).update(**changes)
    for entry in DATA["materials"]:
        Material.objects.using(alias).filter(code=entry["code"], name=entry["name"], name_en="").update(name_en=entry["name_en"])


class Migration(migrations.Migration):
    dependencies = [("catalog", "0012_material_name_en_product_construction_en_and_more")]
    operations = [migrations.RunPython(populate_english, migrations.RunPython.noop)]
