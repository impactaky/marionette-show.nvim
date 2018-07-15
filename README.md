# marionette-show.nvim

Neovim plugin for opening web browser

## Install

### Common

Install selenium module
```
pip install selenium
```

### Firefox

Install geckodriver
https://github.com/mozilla/geckodriver/releases

### Chrome

Install ChromeDriver
http://chromedriver.chromium.org/downloads


## Usage: Standalone Mode

### Chrome

```.vim
let g:marionette_show#driver_type='Chrome'
```

### Firefox

```.vim
let g:marionette_show#driver_type='Firefox'
```

## Usage: Resume Mode

### Chrome

```.vim
let g:marionette_show#driver_type='Chrome'
let g:marionette_show#remote#enable=1
let g:marionette_show#remote#url='http://localhost:9515'
let g:marionette_show#remote#resume#enable=1
```

### Firefox

```.vim
let g:marionette_show#driver_type='Chrome'
let g:marionette_show#remote#enable=1
let g:marionette_show#remote#url='http://localhost:4444'
let g:marionette_show#remote#resume#enable=1
```
