# bubblecheck
[![Build Status](https://travis-ci.org/taylorreece/bubblecheck.svg?branch=master)](https://travis-ci.org/taylorreece/bubblecheck)

This repo contains all the code we'll need for the BubbleCheck rewrite.

* bubblecheck/ contains web front-end stuff and API stuff
* bubblecheck-vue/ contains vue code that gets placed into bubblecheck/templates and bubblecheck/static at build time
* aws/ contains lambda functions, cloudformation information, etc.

To run the vue frontend live, 
 $ cd bubblecheck-vue
 $ npm run dev

To build it,
 $ npm run build