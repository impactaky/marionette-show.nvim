if exists('g:loaded_marionette_show')
	finish
endif
let g:loaded_marionette_show = 1

if !exists('g:marionette_show#driver_type')
	let g:marionette_show#driver_type = 0
endif
if !exists('g:marionette_show#remote#enable')
	let g:marionette_show#remote#enable = 0
endif
if !exists('g:marionette_show#remote#url')
	let g:marionette_show#remote#url = 'https://localhost'
endif
if !exists('g:marionette_show#resume#enable')
	let g:marionette_show#resume#enable = 0
endif

