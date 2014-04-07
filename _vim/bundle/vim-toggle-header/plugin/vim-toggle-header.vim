if !exists("g:vim_toggle_header_loaded")
python << EOF
import sys, vim
sys.path.append(vim.eval("expand('<sfile>:p:h')"))
import vim_toggle_header
EOF
let g:vim_toggle_header_loaded = 1
endif

nn <leader>o :py vim_toggle_header.toggle()<cr>
nn <leader>O :vsp<cr><C-W>l :py vim_toggle_header.toggle()<cr><C-W>h

