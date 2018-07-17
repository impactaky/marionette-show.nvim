function! marionette_show#denite#action#open_in_browser(context)
	call _marionette_get(join(['file://', a:context['path']], ''))
endfunction
