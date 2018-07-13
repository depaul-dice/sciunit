set _sciunit_ls_py = 'import sciunit2.workspace; print " ".join(["e%d" % x for x in sciunit2.workspace.current()[0]._ExecutionManager__f.keys()])'
set _sciunit_articles_py = 'import sciunit2.workspace; import sciunit2.config; print " ".join([x[9:-1] for x in sciunit2.config.Config(sciunit2.workspace.current()[1].location+"/config").keys()])'
complete -sciu* 'p/0/(sciunit)/'
complete sciunit \
  'C/--/(--help --version --setup --file)/' \
  'C/-/(-m -i -n --setup --file)/' \
  'p/1/(create open exec repeat list show \
        given commit rm sort push copy gc)/' \
  'n/create/x:<sciunit name>/' \
  'N/create/n/' \
  "n@open@D:$HOME/sciunit/@ @" \
  'n/-m/x:<new sciunit name>/' \
  'N/-m/n/' \
  'n/exec/c/' \
  'n/-i/n/' \
  'n/repeat/`python -c "$_sciunit_ls_py"`/' \
  'n/list/n/' \
  'n/show/`python -c "$_sciunit_ls_py"`/' \
  'N/show/n/' \
  'N/given/(repeat exec)/' \
  'n/commit/n/' \
  'n/rm/x:eN[-M]/' \
  'N/rm/n/' \
  'n/sort/x:<execution ids...>/' \
  'n/--file/f/' \
  'N/--file/n/' \
  'n/push/`python -c "$_sciunit_articles_py"`/' \
  'N/push/(--setup --file --)/' \
  'n/--setup/(hs hydroshare fs figshare)/' \
  'N/--setup/n/' \
  'n/copy/(-n --)/' \
  'n/-n/n/' \

