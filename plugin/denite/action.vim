if exists('denite#custom#action')
	call denite#custom#action(
				\ 'file',
				\ 'open_in_browser', {context ->
				\		_marionette_get(join(['file://',context['path']], ''))})
endif
