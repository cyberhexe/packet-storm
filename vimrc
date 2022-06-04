scriptencoding utf-8
set encoding=utf-8

let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

set nocompatible

map <ScrollWheelUp> <C-Y><C-Y><C-Y>
map <ScrollWheelDown> <C-E><C-E><C-E>
set mouse=a
set background=dark
set incsearch
set hlsearch
syntax enable
set number
set smartindent
set tabstop=8
set shiftwidth=8
"set expandtab
set nowrap
set path+=**
set wildmenu
if &diff
syntax off
endif
set listchars=trail:·,tab:▸\
set list
hi SpecialKey ctermfg=237
set colorcolumn=120
hi colorcolumn ctermbg=237


" Makes the 81st and 101st column grey
hi colorcolumn ctermbg=236 guibg=#3a3a3a
" set colorcolumn=81,101

autocmd FileType markdown,gitcommit setlocal spell

hi ma1 ctermbg=darkred ctermfg=white guibg=darkblue guifg=white
hi ma2 ctermbg=darkgreen ctermfg=white guibg=darkgreen guifg=white
hi ma3 ctermbg=darkyellow ctermfg=white guibg=darkyellow guifg=white

" Copy selected text when with right click
vmap <RightMouse> :call CopySelected()<CR>
function CopySelected()
	let @+ = @*
endfunction

" Hilighting multiple words using multiple colors
vmap 1 :call HiSelection("ma1", 1)<CR>
vmap 2 :call HiSelection("ma2", 2)<CR>
vmap 3 :call HiSelection("ma3", 3)<CR>
vmap ;1 :call matchdelete(1 + 3)<CR>
vmap ;2 :call matchdelete(2 + 3)<CR>
vmap ;3 :call matchdelete(3 + 3)<CR>

function HiSelection(group, id)
	let str = getline("'<")[getpos("'<")[2]-1:getpos("'>")[2]-1]
	let str = "\\<" . str . "\\>"
	echom str
	call matchadd(a:group, str, 10, a:id + 3)
endfunction


autocmd FileType markdown,gitcommit setlocal spell


" sudo apt-get install vim-gui-common
" sudo apt-get install vim-runtime

call plug#begin()
" The default plugin directory will be as follows:
"   - Vim (Linux/macOS): '~/.vim/plugged'
"   - Vim (Windows): '~/vimfiles/plugged'
"   - Neovim (Linux/macOS/Windows): stdpath('data') . '/plugged'
" You can specify a custom plugin directory by passing it as the argument
"   - e.g. `call plug#begin('~/.vim/plugged')`
"   - Avoid using standard Vim directory names like 'plugin'

" Make sure you use single quotes

Plug 'ekalinin/Dockerfile.vim'

" Shorthand notation; fetches https://github.com/junegunn/vim-easy-align
Plug 'junegunn/vim-easy-align'

" Any valid git URL is allowed
Plug 'https://github.com/junegunn/vim-github-dashboard.git'

" Multiple Plug commands can be written in a single line using | separators
Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

" On-demand loading
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }

" Using a non-default branch
Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }

" Using a tagged release; wildcard allowed (requires git 1.9.2 or above)
Plug 'fatih/vim-go', { 'tag': '*' }

" Plugin options
Plug 'nsf/gocode', { 'tag': 'v.20150303', 'rtp': 'vim' }

" Plugin outside ~/.vim/plugged with post-update hook
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

" Unmanaged plugin (manually installed and updated)
Plug '~/my-prototype-plugin'

" Initialize plugin system
call plug#end()

