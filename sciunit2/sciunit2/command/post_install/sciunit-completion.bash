_sciunit_contains ()
{
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

_sciunit ()
{
  _sciunit_ls_py='import sciunit2.workspace; print " ".join(["e%d" % x for x in sciunit2.workspace.current()[0]._ExecutionManager__f.keys()])'
  _sciunit_articles_py='import sciunit2.workspace; import sciunit2.config; print " ".join([x[9:-1] for x in sciunit2.config.Config(sciunit2.workspace.current()[1].location+"/config").keys()])'

  local cur prev preN untilN
  _init_completion || return

  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  preN="${COMP_WORDS[COMP_CWORD-2]}"

  case "$cur" in
    --*)
    COMPREPLY=( $( compgen -W '--help --version --setup --file' -- $cur ) )
    return;;
    -*)
    COMPREPLY=( $( compgen -W '-m -i -n --setup --file' -- $cur ) )
    return;;
  esac

  if [[ "$COMP_CWORD" -eq 1 ]]; then
    COMPREPLY=( $( compgen -W 'create open exec repeat list show \
                               given commit rm sort push copy gc' -- $cur ) )
    return
  fi

  case "$prev" in
    open)
    local IFS=$'\n'
    compopt -o filenames
    COMPREPLY=( $( cd ~/sciunit && compgen -A directory -- $cur ) )
    return;;
    exec)
    COMPREPLY=( $( compgen -A command -- $cur ) )
    return;;
    repeat|show)
    COMPREPLY=( $( compgen -W "$(python -c "$_sciunit_ls_py")" -- $cur ) )
    return;;
    given)
    _filedir
    return;;
    push)
    COMPREPLY=( $( compgen -W "$(python -c "$_sciunit_articles_py")" -- $cur ) )
    return;;
    --setup)
    COMPREPLY=( $( compgen -W 'hs hydroshare fs figshare' -- $cur ) )
    return;;
    --file)
    _filedir
    return;;
    -i)
    return;;
  esac

  case "$preN" in
    given)
    COMPREPLY=( $( compgen -W 'repeat exec' -- $cur ) )
    return;;
    push)
    COMPREPLY=( $( compgen -W '--setup --file --' -- $cur ) )
    return;;
    copy)
    COMPREPLY=( $( compgen -W '-n --' -- $cur ) )
    return;;
  esac

  if [[ $((COMP_CWORD-2)) -gt 0 ]]; then
    untilN=("${COMP_WORDS[@]:1:$((COMP_CWORD-1))}")
    if _sciunit_contains "exec" "${untilN[@]}" || \
       _sciunit_contains "repeat" "${untilN[@]}"; then
      _filedir
    fi
  fi
}

complete -F _sciunit sciunit
