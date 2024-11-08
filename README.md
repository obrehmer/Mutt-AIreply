# Mutt: Reply mails created by Open AI


## Checkout the format.py to .mutt/format.py

## Create a wrapper .mutt/email_file

```
#!/usr/bin/env bash

message=$(cat)

echo "${message}" | ~/.mutt/format.py > "/tmp/xxx"

```

## and .mutt/aireply

```
#!/bin/bash
vim $1 "+:call AIReply()"
```

## Make all the snippets executable

```
chmod +x .mutt/format.py  .mutt/email_file .mutt/aireply
```


## Insert  a function in the .vimrc

```
function! AIReply()
  %d_
  r /tmp/xxx
  0d_
  w
endfunction

```
## Add 2 macros to the .muttrc

```
macro index,pager S "| ~/.mutt/email_file <enter>"
macro index,pager A "<enter-command>set editor=~/.mutt/aireply<enter><reply><edit-from><kill-line>Do Not Reply <noreply@domain.tld><enter><edit-subject><bol><delete-char><delete-char><delete-char><delete-char>Automatic Reply (was: <eol>)<enter><send-message>a<enter-command>set editor=vim<enter>" "Auto-reply + archive"
```


## Usage

Open the mail you want to reply an Press "S". It will create the template in /tmp/xxx (or a more save place you define in .mutt/email_file).
After that you can simply press "A" and the AI generated mail appears in the editor mode in mutt. Just send it now. 


