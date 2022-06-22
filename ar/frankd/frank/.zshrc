#!/usr/bin/env zsh

skip_global_compinit=1
autoload -Uz compinit && compinit -u
autoload -Uz colors && colors

typeset -gx COLORTERM=truecolor
typeset -gx TERM=xterm-256color

typeset -g HISTSIZE=50000
typeset -g SAVEHIST=45000
typeset -g HISTFILE=/var/data/cache/.zsh_history
typeset -g HISTSTAMPS='yyyy-mm-dd'

typeset -gx LANG=en_US.UTF-8
# typeset -gx LC_ALL=en_US.UTF-8
typeset -gx LC_CTYPE=en_US.UTF-8
typeset -gx LS_COLORS='bd=38;5;68:ca=38;5;17:cd=38;5;113;1:di=38;5;30:do=38;5;127:ex=38;5;208;1:pi=38;5;126:fi=0:ln=target:mh=38;5;222;1:no=0:or=48;5;196;38;5;232;1:ow=38;5;220;1:sg=48;5;3;38;5;0:su=38;5;220;1;3;100;1:so=38;5;197:st=38;5;86;48;5;234:tw=48;5;235;38;5;139;3:*LS_COLORS=48;5;89;38;5;197;1;3;4;7:*README=38;5;220;1:*README.rst=38;5;220;1:*README.md=38;5;220;1:*LICENSE=38;5;220;1:*COPYING=38;5;220;1:*INSTALL=38;5;220;1:*COPYRIGHT=38;5;220;1:*AUTHORS=38;5;220;1:*HISTORY=38;5;220;1:*CONTRIBUTORS=38;5;220;1:*PATENTS=38;5;220;1:*VERSION=38;5;220;1:*NOTICE=38;5;220;1:*CHANGES=38;5;220;1:*.log=38;5;190:*.txt=38;5;253:*.adoc=38;5;184:*.asciidoc=38;5;184:*.etx=38;5;184:*.info=38;5;184:*.markdown=38;5;184:*.md=38;5;184:*.mkd=38;5;184:*.nfo=38;5;184:*.pod=38;5;184:*.rst=38;5;184:*.tex=38;5;184:*.textile=38;5;184:*.bib=38;5;178:*.json=38;5;178:*.jsonl=38;5;178:*.jsonnet=38;5;178:*.libsonnet=38;5;142:*.ndjson=38;5;178:*.msg=38;5;178:*.pgn=38;5;178:*.rss=38;5;178:*.xml=38;5;178:*.fxml=38;5;178:*.toml=38;5;178:*.yaml=38;5;178:*.yml=38;5;178:*.RData=38;5;178:*.rdata=38;5;178:*.xsd=38;5;178:*.dtd=38;5;178:*.sgml=38;5;178:*.rng=38;5;178:*.rnc=38;5;178:*.cbr=38;5;141:*.cbz=38;5;141:*.chm=38;5;141:*.djvu=38;5;141:*.pdf=38;5;141:*.PDF=38;5;141:*.mobi=38;5;141:*.epub=38;5;141:*.docm=38;5;111;4:*.doc=38;5;111:*.docx=38;5;111:*.odb=38;5;111:*.odt=38;5;111:*.rtf=38;5;111:*.odp=38;5;166:*.pps=38;5;166:*.ppt=38;5;166:*.pptx=38;5;166:*.ppts=38;5;166:*.pptxm=38;5;166;4:*.pptsm=38;5;166;4:*.csv=38;5;78:*.tsv=38;5;78:*.ods=38;5;112:*.xla=38;5;76:*.xls=38;5;112:*.xlsx=38;5;112:*.xlsxm=38;5;112;4:*.xltm=38;5;73;4:*.xltx=38;5;73:*.pages=38;5;111:*.numbers=38;5;112:*.key=38;5;166:*config=1:*cfg=1:*conf=1:*rc=1:*authorized_keys=1:*known_hosts=1:*.ini=1:*.plist=1:*.profile=1:*.bash_profile=1:*.bash_login=1:*.bash_logout=1:*.zshenv=1:*.zprofile=1:*.zlogin=1:*.zlogout=1:*.viminfo=1:*.pcf=1:*.psf=1:*.hidden-color-scheme=1:*.hidden-tmTheme=1:*.last-run=1:*.merged-ca-bundle=1:*.sublime-build=1:*.sublime-commands=1:*.sublime-keymap=1:*.sublime-settings=1:*.sublime-snippet=1:*.sublime-project=1:*.sublime-workspace=1:*.tmTheme=1:*.user-ca-bundle=1:*.rstheme=1:*.epf=1:*.git=38;5;197:*.gitignore=38;5;240:*.gitattributes=38;5;240:*.gitmodules=38;5;240:*.awk=38;5;172:*.bash=38;5;172:*.bat=38;5;172:*.BAT=38;5;172:*.sed=38;5;172:*.sh=38;5;172:*.zsh=38;5;172:*.vim=38;5;172:*.kak=38;5;172:*.ahk=38;5;41:*.py=38;5;41:*.ipynb=38;5;41:*.rb=38;5;41:*.gemspec=38;5;41:*.pl=38;5;208:*.PL=38;5;160:*.t=38;5;114:*.msql=38;5;222:*.mysql=38;5;222:*.pgsql=38;5;222:*.sql=38;5;222:*.tcl=38;5;64;1:*.r=38;5;49:*.R=38;5;49:*.gs=38;5;81:*.clj=38;5;41:*.cljs=38;5;41:*.cljc=38;5;41:*.cljw=38;5;41:*.scala=38;5;41:*.sc=38;5;41:*.dart=38;5;51:*.asm=38;5;81:*.cl=38;5;81:*.lisp=38;5;81:*.rkt=38;5;81:*.lua=38;5;81:*.moon=38;5;81:*.c=38;5;81:*.C=38;5;81:*.h=38;5;110:*.H=38;5;110:*.tcc=38;5;110:*.c++=38;5;81:*.h++=38;5;110:*.hpp=38;5;110:*.hxx=38;5;110:*.ii=38;5;110:*.M=38;5;110:*.m=38;5;110:*.cc=38;5;81:*.cs=38;5;81:*.cp=38;5;81:*.cpp=38;5;81:*.cxx=38;5;81:*.cr=38;5;81:*.go=38;5;81:*.f=38;5;81:*.F=38;5;81:*.for=38;5;81:*.ftn=38;5;81:*.f90=38;5;81:*.F90=38;5;81:*.f95=38;5;81:*.F95=38;5;81:*.f03=38;5;81:*.F03=38;5;81:*.f08=38;5;81:*.F08=38;5;81:*.nim=38;5;81:*.nimble=38;5;81:*.s=38;5;110:*.S=38;5;110:*.rs=38;5;81:*.scpt=38;5;219:*.swift=38;5;219:*.sx=38;5;81:*.vala=38;5;81:*.vapi=38;5;81:*.hi=38;5;110:*.hs=38;5;81:*.lhs=38;5;81:*.agda=38;5;81:*.lagda=38;5;81:*.lagda.tex=38;5;81:*.lagda.rst=38;5;81:*.lagda.md=38;5;81:*.agdai=38;5;110:*.zig=38;5;81:*.v=38;5;81:*.pyc=38;5;240:*.tf=38;5;168:*.tfstate=38;5;168:*.tfvars=38;5;168:*.css=38;5;125;1:*.less=38;5;125;1:*.sass=38;5;125;1:*.scss=38;5;125;1:*.htm=38;5;125;1:*.html=38;5;125;1:*.jhtm=38;5;125;1:*.mht=38;5;125;1:*.eml=38;5;125;1:*.mustache=38;5;125;1:*.coffee=38;5;074;1:*.java=38;5;074;1:*.js=38;5;074;1:*.mjs=38;5;074;1:*.jsm=38;5;074;1:*.jsp=38;5;074;1:*.php=38;5;81:*.ctp=38;5;81:*.twig=38;5;81:*.vb=38;5;81:*.vba=38;5;81:*.vbs=38;5;81:*Dockerfile=38;5;155:*.dockerignore=38;5;240:*Makefile=38;5;155:*MANIFEST=38;5;243:*pm_to_blib=38;5;240:*.nix=38;5;155:*.dhall=38;5;178:*.rake=38;5;155:*.am=38;5;242:*.in=38;5;242:*.hin=38;5;242:*.scan=38;5;242:*.m4=38;5;242:*.old=38;5;242:*.out=38;5;242:*.SKIP=38;5;244:*.diff=48;5;197;38;5;232:*.patch=48;5;197;38;5;232;1:*.bmp=38;5;97:*.dicom=38;5;97:*.tiff=38;5;97:*.tif=38;5;97:*.TIFF=38;5;97:*.cdr=38;5;97:*.flif=38;5;97:*.gif=38;5;97:*.icns=38;5;97:*.ico=38;5;97:*.jpeg=38;5;97:*.JPG=38;5;97:*.jpg=38;5;97:*.nth=38;5;97:*.png=38;5;97:*.psd=38;5;97:*.pxd=38;5;97:*.pxm=38;5;97:*.xpm=38;5;97:*.webp=38;5;97:*.ai=38;5;99:*.eps=38;5;99:*.epsf=38;5;99:*.drw=38;5;99:*.ps=38;5;99:*.svg=38;5;99:*.avi=38;5;114:*.divx=38;5;114:*.IFO=38;5;114:*.m2v=38;5;114:*.m4v=38;5;114:*.mkv=38;5;114:*.MOV=38;5;114:*.mov=38;5;114:*.mp4=38;5;114:*.mpeg=38;5;114:*.mpg=38;5;114:*.ogm=38;5;114:*.rmvb=38;5;114:*.sample=38;5;114:*.wmv=38;5;114:*.3g2=38;5;115:*.3gp=38;5;115:*.gp3=38;5;115:*.webm=38;5;115:*.gp4=38;5;115:*.asf=38;5;115:*.flv=38;5;115:*.ts=38;5;115:*.ogv=38;5;115:*.f4v=38;5;115:*.VOB=38;5;115;1:*.vob=38;5;115;1:*.ass=38;5;117:*.srt=38;5;117:*.ssa=38;5;117:*.sub=38;5;117:*.sup=38;5;117:*.vtt=38;5;117:*.3ga=38;5;137;1:*.S3M=38;5;137;1:*.aac=38;5;137;1:*.amr=38;5;137;1:*.au=38;5;137;1:*.caf=38;5;137;1:*.dat=38;5;137;1:*.dts=38;5;137;1:*.fcm=38;5;137;1:*.m4a=38;5;137;1:*.mod=38;5;137;1:*.mp3=38;5;137;1:*.mp4a=38;5;137;1:*.oga=38;5;137;1:*.ogg=38;5;137;1:*.opus=38;5;137;1:*.s3m=38;5;137;1:*.sid=38;5;137;1:*.wma=38;5;137;1:*.ape=38;5;136;1:*.aiff=38;5;136;1:*.cda=38;5;136;1:*.flac=38;5;136;1:*.alac=38;5;136;1:*.mid=38;5;136;1:*.midi=38;5;136;1:*.pcm=38;5;136;1:*.wav=38;5;136;1:*.wv=38;5;136;1:*.wvc=38;5;136;1:*.afm=38;5;66:*.fon=38;5;66:*.fnt=38;5;66:*.pfb=38;5;66:*.pfm=38;5;66:*.ttf=38;5;66:*.otf=38;5;66:*.woff=38;5;66:*.woff2=38;5;66:*.PFA=38;5;66:*.pfa=38;5;66:*.7z=38;5;40:*.a=38;5;40:*.arj=38;5;40:*.bz2=38;5;40:*.cpio=38;5;40:*.gz=38;5;40:*.lrz=38;5;40:*.lz=38;5;40:*.lzma=38;5;40:*.lzo=38;5;40:*.rar=38;5;40:*.s7z=38;5;40:*.sz=38;5;40:*.tar=38;5;40:*.tbz=38;5;40:*.tgz=38;5;40:*.warc=38;5;40:*.WARC=38;5;40:*.xz=38;5;40:*.z=38;5;40:*.zip=38;5;40:*.zipx=38;5;40:*.zoo=38;5;40:*.zpaq=38;5;40:*.zst=38;5;40:*.zstd=38;5;40:*.zz=38;5;40:*.apk=38;5;215:*.ipa=38;5;215:*.deb=38;5;215:*.rpm=38;5;215:*.jad=38;5;215:*.jar=38;5;215:*.ear=38;5;215:*.war=38;5;215:*.cab=38;5;215:*.pak=38;5;215:*.pk3=38;5;215:*.vdf=38;5;215:*.vpk=38;5;215:*.bsp=38;5;215:*.dmg=38;5;215:*.crx=38;5;215:*.xpi=38;5;215:*.r[0-9]{0,2}=38;5;239:*.zx[0-9]{0,2}=38;5;239:*.z[0-9]{0,2}=38;5;239:*.part=38;5;239:*.iso=38;5;124:*.bin=38;5;124:*.nrg=38;5;124:*.qcow=38;5;124:*.sparseimage=38;5;124:*.toast=38;5;124:*.vcd=38;5;124:*.vmdk=38;5;124:*.accdb=38;5;60:*.accde=38;5;60:*.accdr=38;5;60:*.accdt=38;5;60:*.db=38;5;60:*.fmp12=38;5;60:*.fp7=38;5;60:*.localstorage=38;5;60:*.mdb=38;5;60:*.mde=38;5;60:*.sqlite=38;5;60:*.typelib=38;5;60:*.nc=38;5;60:*.pacnew=38;5;33:*.un~=38;5;241:*.orig=38;5;241:*.BUP=38;5;241:*.bak=38;5;241:*.o=38;5;241:*core=38;5;241:*.mdump=38;5;241:*.rlib=38;5;241:*.dll=38;5;241:*.swp=38;5;244:*.swo=38;5;244:*.tmp=38;5;244:*.sassc=38;5;244:*.pid=38;5;248:*.state=38;5;248:*lockfile=38;5;248:*lock=38;5;248:*.err=38;5;160;1:*.error=38;5;160;1:*.stderr=38;5;160;1:*.aria2=38;5;241:*.dump=38;5;241:*.stackdump=38;5;241:*.zcompdump=38;5;241:*.zwc=38;5;241:*.pcap=38;5;29:*.cap=38;5;29:*.dmp=38;5;29:*.DS_Store=38;5;239:*.localized=38;5;239:*.CFUserTextEncoding=38;5;239:*.allow=38;5;112:*.deny=38;5;196:*.service=38;5;45:*@.service=38;5;45:*.socket=38;5;45:*.swap=38;5;45:*.device=38;5;45:*.mount=38;5;45:*.automount=38;5;45:*.target=38;5;45:*.path=38;5;45:*.timer=38;5;45:*.snapshot=38;5;45:*.application=38;5;116:*.cue=38;5;116:*.description=38;5;116:*.directory=38;5;116:*.m3u=38;5;116:*.m3u8=38;5;116:*.md5=38;5;116:*.properties=38;5;116:*.sfv=38;5;116:*.theme=38;5;116:*.torrent=38;5;116:*.urlview=38;5;116:*.webloc=38;5;116:*.lnk=38;5;39:*CodeResources=38;5;239:*PkgInfo=38;5;239:*.nib=38;5;57:*.car=38;5;57:*.dylib=38;5;241:*.entitlements=1:*.pbxproj=1:*.strings=1:*.storyboard=38;5;196:*.xcconfig=1:*.xcsettings=1:*.xcuserstate=1:*.xcworkspacedata=1:*.xib=38;5;208:*.asc=38;5;192;3:*.bfe=38;5;192;3:*.enc=38;5;192;3:*.gpg=38;5;192;3:*.signature=38;5;192;3:*.sig=38;5;192;3:*.p12=38;5;192;3:*.pem=38;5;192;3:*.pgp=38;5;192;3:*.p7s=38;5;192;3:*id_dsa=38;5;192;3:*id_rsa=38;5;192;3:*id_ecdsa=38;5;192;3:*id_ed25519=38;5;192;3:*.32x=38;5;213:*.cdi=38;5;213:*.fm2=38;5;213:*.rom=38;5;213:*.sav=38;5;213:*.st=38;5;213:*.a00=38;5;213:*.a52=38;5;213:*.A64=38;5;213:*.a64=38;5;213:*.a78=38;5;213:*.adf=38;5;213:*.atr=38;5;213:*.gb=38;5;213:*.gba=38;5;213:*.gbc=38;5;213:*.gel=38;5;213:*.gg=38;5;213:*.ggl=38;5;213:*.ipk=38;5;213:*.j64=38;5;213:*.nds=38;5;213:*.nes=38;5;213:*.sms=38;5;213:*.8xp=38;5;121:*.8eu=38;5;121:*.82p=38;5;121:*.83p=38;5;121:*.8xe=38;5;121:*.stl=38;5;216:*.dwg=38;5;216:*.ply=38;5;216:*.wrl=38;5;216:*.pot=38;5;7:*.pcb=38;5;7:*.mm=38;5;7:*.gbr=38;5;7:*.scm=38;5;7:*.xcf=38;5;7:*.spl=38;5;7:*.Rproj=38;5;11:*.sis=38;5;7:*.1p=38;5;7:*.3p=38;5;7:*.cnc=38;5;7:*.def=38;5;7:*.ex=38;5;7:*.example=38;5;7:*.feature=38;5;7:*.ger=38;5;7:*.ics=38;5;7:*.map=38;5;7:*.mf=38;5;7:*.mfasl=38;5;7:*.mi=38;5;7:*.mtx=38;5;7:*.pc=38;5;7:*.pi=38;5;7:*.plt=38;5;7:*.pm=38;5;7:*.rdf=38;5;7:*.ru=38;5;7:*.sch=38;5;7:*.sty=38;5;7:*.sug=38;5;7:*.tdy=38;5;7:*.tfm=38;5;7:*.tfnt=38;5;7:*.tg=38;5;7:*.vcard=38;5;7:*.vcf=38;5;7:*.xln=38;5;7:*.iml=38;5;166:';

typeset -gra IGNORES=(
  .bzr CVS .git .hg .svn
  .idea .tox .env
  .ven ven .venv venv
  .npm node_modules
)

typeset -grA CFG_ZSH_KEY=(
  Insert    "${terminfo[kich1]}"
  Delete    "${terminfo[kdch1]}" Control-Delete    "${terminfo[kDC5]}"
  Home      "${terminfo[khome]}" Control-Home      "${terminfo[kHOM5]}"
  End       "${terminfo[kend]}"  Control-End       "${terminfo[kEND5]}"
  PageUp    "${terminfo[kpp]}"   Control-PageUp    "${terminfo[kPRV5]}"
  PageDown  "${terminfo[knp]}"   Control-PageDown  "${terminfo[kNXT5]}"
  Up        "${terminfo[kcuu1]}" Control-Up        "${terminfo[kUP5]}"
  Down      "${terminfo[kcud1]}" Control-Down      "${terminfo[kDN5]}"
  Left      "${terminfo[kcub1]}" Control-Left      "${terminfo[kLFT5]}"
  Right     "${terminfo[kcuf1]}" Control-Right     "${terminfo[kRIT5]}"
  F1        "${terminfo[kf1]}"   F6                "${terminfo[kf6]}"
  F2        "${terminfo[kf2]}"   F7                "${terminfo[kf7]}"
  F3        "${terminfo[kf3]}"   F8                "${terminfo[kf8]}"
  F4        "${terminfo[kf4]}"   F9                "${terminfo[kf9]}"
  F5        "${terminfo[kf5]}"   F10               "${terminfo[kf10]}"
  Control-F1 '^[[1;5P' Control-F2 '^[[1;5Q'
  Control-F3 '^[[1;5R' Control-F4 '^[[1;5S'
  Control-A '^a' Control-G '^g' Control-M '^m' Control-S '^s' Control-Y '^y'
  Control-B '^b' Control-H '^h' Control-N '^n' Control-T '^t' Control-Z '^z'
  Control-C '^c' Control-I '^i' Control-O '^o' Control-U '^u'
  Control-D '^d' Control-J '^j' Control-P '^p' Control-V '^v'
  Control-E '^e' Control-K '^k' Control-Q '^q' Control-W '^w'
  Control-F '^f' Control-L '^l' Control-R '^r' Control-X '^x'
  Control-0 "^0" Control-5 "^5"
  Control-1 "^1" Control-6 "^6"
  Control-2 "^2" Control-7 "^7"
  Control-3 "^3" Control-8 "^8"
  Control-4 "^4" Control-9 "^9"
  Escape    '\e'
  Shift-Tab "${terminfo[kcbt]}"
  Backspace "${terminfo[kbs]}"   Control-Backspace '^H'
)

setopt AUTO_CD
setopt AUTO_NAME_DIRS
setopt CDABLE_VARS
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt PUSHDMINUS
setopt HASH_CMDS
setopt HASH_DIRS
setopt PATH_DIRS
setopt SHORT_LOOPS
setopt PUSHD_SILENT
setopt PUSHD_TO_HOME
setopt MULTIOS
setopt EXTENDED_GLOB
setopt AUTO_PARAM_SLASH
unsetopt CLOBBER
setopt PROMPT_SUBST
setopt PROMPT_SP
setopt AUTO_MENU
setopt AUTO_LIST
setopt NO_BEEP
setopt NO_CHASE_LINKS
setopt NO_RM_STAR_SILENT
setopt ALWAYS_TO_END
setopt COMPLETE_IN_WORD
setopt NO_COMPLETE_ALIASES
setopt APPEND_HISTORY
setopt BANG_HIST
setopt EXTENDED_HISTORY
setopt HIST_BEEP
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_REDUCE_BLANKS
setopt HIST_SAVE_NO_DUPS
setopt HIST_VERIFY
setopt INC_APPEND_HISTORY
setopt SHARE_HISTORY

zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path $ZCOMPCACHE
zstyle ':completion:*' verbose yes
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' insert-tab pending
zstyle ':completion:*' squeeze-slashes true
zstyle ':completion:*' special-dirs true
zstyle ':completion:*' expand yes
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' menu select=2 _complete _approximate _ignored
zstyle ':completion:*' accept-exact "*(N)"
zstyle ':completion:*:options' description 'yes'
zstyle ':completion:*:options' auto-description '%d'
zstyle ':completion:*:default' list-prompt '%S%M matches%s'
zstyle ':completion:*:matches' group 'yes'
zstyle ':completion:*:match:*' original only
zstyle ':completion:*:approximate:*' max-errors 'reply=( $(( ($#PREFIX+$#SUFFIX)/3 )) numeric )'
zstyle ':completion:*::::' completer _expand _complete _approximate _ignored
zstyle ':completion:*:functions' ignored-patterns '_*' 'pre(cmd|exec)'
zstyle ':completion:*' format ' %F{186}-- %d --%f'
zstyle ':completion:*:messages' format ' %F{116}-- %d --%f'
zstyle ':completion:*:descriptions' format ' %F{221}-- %d --%f'
zstyle ':completion:*:corrections' format ' %F{202}-- %d (errors: %e) --%f'
zstyle ':completion:*:warnings' format ' %F{228}-- no matches found --%f'
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*:default' list-colors '=(#b)*(-- *)=2;38;5;246=2;38;5;240' '=*=2;38;5;246'

# -- custom --------------------------------------------------------------------

reload() {
  exec ${SHELL#-}
}

command!() {
  command -v $1 > /dev/null 2>&1
}

+command!() {
  (( $+commands[$1] )) || return 1
}

+function!() {
  (( $+functions[$1] )) || return 1
}

+fx!() {
  (( $+functions[$1] )) && eval $1
}

bindkeyr!() {
  local key value
  local -A mapping=(${(Pkv)@})
  for key value in ${(kv)mapping}; do
    [[ -z ${CFG_ZSH_KEY[$key]} ]] || key=${CFG_ZSH_KEY[$key]}
    bindkey -M emacs $key $value
  done
}

autoload edit-command-line; zle -N edit-command-line

prompt_minimal_setup() {
  ZTHEME='minimal'
  prompt_opts=(cr percent sp subst)
  PROMPT=' %(?:%F{042}:%F{203})(ds)%f%F{245}:%f '
  RPROMPT=' %F{240}%64<...<%~%<<%f '
  echo -ne '\e[5 q'
}

# -- set -----------------------------------------------------------------------

function {
  local -A mapping=(
    Backspace         'backward-delete-char'
    Home              'beginning-of-line'
    End               'end-of-line'
    Insert            'overwrite-mode'
    Delete            'delete-char'
    Up                'up-line-or-history'
    Down              'down-line-or-history'
    Left              'backward-char'
    Right             'forward-char'
    PageUp            'beginning-of-buffer-or-history'
    PageDown          'end-of-buffer-or-history'
    Control-Up        'up-line-or-search'
    Control-Down      'down-line-or-search'
    Control-Left      'backward-word'
    Control-Right     'forward-word'
    Control-Backspace 'backward-kill-word'
    Control-Delete    'kill-word'
    Shift-Tab         'reverse-menu-complete'
    Control-E         'edit-command-line'
  )
  bindkeyr! mapping
}

if (( ${+terminfo[smkx]} && ${+terminfo[rmkx]} )); then
  autoload -Uz add-zle-hook-widget
  function zle_application_mode_start { echoti smkx }
  function zle_application_mode_stop { echoti rmkx }
  add-zle-hook-widget -Uz zle-line-init zle_application_mode_start
  add-zle-hook-widget -Uz zle-line-finish zle_application_mode_stop
fi

prompt_minimal_setup "$@"

alias _=sudo
alias sudoe='sudo -E'
alias :q='exit'
alias quit='exit'
alias c='clear'
alias cl='clear;ls'
alias cpl='clear;pwd;ls'

alias cp='cp -i'
alias rm='rm -i'
alias mv='mv -i'
alias mkdir='mkdir -p'

alias dk=docker
alias dps='docker ps -a'
alias dim='docker images'
alias drmx='docker rm -f $(docker ps -qa)'
alias drmc='docker rm $(docker ps -qaf status=exited)'
alias drmi='docker rmi $(docker images -qf dangling=true)'
alias drmv='docker volume rm $(docker volume ls -qf dangling=true)'
alias drms='docker service rm $(docker service ls -q)'
alias drmc='docker config rm $(docker config ls -q)'
alias drmt='docker secret rm $(docker secret ls -q)'
alias drma='drmt; drmc; drms'

alias gs='git status --porcelain --branch'
alias gss='git status --porcelain=v2 --branch'
alias glo='git log --oneline'
alias grso='git remote show origin'
alias gru='git config --get remote.origin.url'

function {
  local ls_opts
  ls_opts+='-lv --classify --group-directories-first '
  ls_opts+='--human-readable --color=always --time-style="+%Y-%m-%d %T"'
  alias la="ls -A ${ls_opts}"
  alias lr="ls -tR ${ls_opts}"
  alias lt="ls -t ${ls_opts}"
  alias l="ls ${ls_opts}"
  alias ll="ls ${ls_opts}"
  alias l.="ls -d ${ls_opts} .*"
}

function {
  local index parents='' dots='.' under='_'
  for index ({1..7}); do
    dots+='.'; under+='_'; parents+='../'
    alias $dots="cd $parents"
    alias $under="cd $parents; pwd; ls"
  done
}

function {
  case $HISTSTAMPS in
    'mm/dd/yyyy'): 'fc -fl 1';;
    'dd.mm.yyyy'): 'fc -El 1';;
    'yyyy-mm-dd'): 'fc -il 1';;
               *): 'fc -l  1';;
  esac
  alias history=$_
  alias h='history'
}

if +command! grep; then
  alias grep="grep --color=always --exclude-dir=\"{${(j.,.)IGNORES}}\""
  alias grepl='grep --line-number'
fi

if +command! tree; then
  alias tree=" tree -v -F -C -I \"${(j.|.)IGNORES}\" --dirsfirst"
  alias treel='tree -L'
  alias tree1='tree -L 1'
  alias tree2='tree -L 2'
  alias tree3='tree -L 3'
  alias tree4='tree -L 4'
  alias tree5='tree -L 5'
fi

alias -g .h='| head'
alias -g .t='| tail'
alias -g .g='| egrep'
alias -g .l='| less'
alias -g .m='| most'
alias -g .w='| wc -l'
alias -g .less='2>&1 | less'
alias -g .cat='2>&1 | cat -a'
alias -g .2null='2> /dev/null'
alias -g .null='> /dev/null 2>&1'
