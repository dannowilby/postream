
FROM node:20

WORKDIR content

# could copy the files to better cache layers
# need to mount the svelte build folder so that we
# can get the compiled data
COPY . .

RUN cd interface && npm install
RUN cd svelte && npm install

CMD cd interface && node interface.js
