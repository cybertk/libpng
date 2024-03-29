# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'conditions': [
      [ 'os_posix == 1 and OS != "mac" and OS != "android"', {
        # Maybe link to system .so once the security concerns are thought
        # through, since we already use it due to GTK.
        'use_system_libpng%': 0,
      }, {  # os_posix != 1 or OS == "mac"
        'use_system_libpng%': 0,
      }],
    ],
  },
  'conditions': [
    ['use_system_libpng==0', {
      'targets': [
        {
          'target_name': 'libpng',
          'dependencies': [
            '<(DEPTH)/third_party/zlib/zlib.gyp:zlib',
          ],
          'defines': [
            'CHROME_PNG_WRITE_SUPPORT',
            'PNG_USER_CONFIG',
          ],
          'sources': [
            'png.c',
            'png.h',
            'pngconf.h',
            'pngerror.c',
            'pnggccrd.c',
            'pngget.c',
            'pngmem.c',
            'pngpread.c',
            'pngread.c',
            'pngrio.c',
            'pngrtran.c',
            'pngrutil.c',
            'pngset.c',
            'pngtrans.c',
            'pngusr.h',
            'pngvcrd.c',
            'pngwio.c',
            'pngwrite.c',
            'pngwtran.c',
            'pngwutil.c',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              '.',
            ],
            'defines': [
              'CHROME_PNG_WRITE_SUPPORT',
              'PNG_USER_CONFIG',
            ],
          },
          'export_dependent_settings': [
            '<(DEPTH)/third_party/zlib/zlib.gyp:zlib',
          ],
          'conditions': [
            ['OS!="win"', {'product_name': 'png'}],
            ['OS=="win"', {
              'type': '<(component)',
            }, {
              # Chromium libpng does not support building as a shared_library
              # on non-Windows platforms.
              'type': 'static_library',
            }],
            ['OS=="win" and component=="shared_library"', {
              'defines': [
                'PNG_BUILD_DLL',
                'PNG_NO_MODULEDEF',
              ],
              'direct_dependent_settings': {
                'defines': [
                  'PNG_USE_DLL',
                ],
              },          
            }],
            # TODO(kyan): set toolsets to host will cause building errors.
            #             What the meaning of |toolsets|?
            #['OS=="android"', {
            #  'toolsets': ['target', 'host'],
            #}],
          ],
        },
      ]
    }, {
      'conditions': [
        ['sysroot!=""', {
          'variables': {
            'pkg-config': '../../build/linux/pkg-config-wrapper "<(sysroot)" "<(target_arch)"',
          },
        }, {
          'variables': {
            'pkg-config': 'pkg-config'
          },
        }],
      ],
      'targets': [
        {
          'target_name': 'libpng',
          'type': 'none',
          'dependencies': [
            '<(DEPTH)/third_party/zlib/zlib.gyp:zlib',
          ],
          'direct_dependent_settings': {
            'cflags': [
              '<!@(<(pkg-config) --cflags libpng)',
            ],
            'defines': [
              'USE_SYSTEM_LIBPNG',
            ],
          },
          'link_settings': {
            'ldflags': [
              '<!@(<(pkg-config) --libs-only-L --libs-only-other libpng)',
            ],
            'libraries': [
              '<!@(<(pkg-config) --libs-only-l libpng)',
            ],
          },
        },
      ],
    }],
  ],
}
