if !exists("g:vim_xcodebuild_loaded")
python << EOF
import sys, vim
sys.path.append(vim.eval("expand('<sfile>:p:h')"))
import vim_xcodebuild
EOF
let g:vim_xcodebuild_loaded = 1
endif

nn <leader>u :py vim_xcodebuild.test()<cr>
nn <leader>b :py vim_xcodebuild.build()<cr>
