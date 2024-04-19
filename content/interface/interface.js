const { spawn } = require('node:child_process');
const express = require('express');
const app = express()

app.get('/', (req, res) => {

  // checks if windows or linux
  const build = spawn(/^win/.test(process.platform) ? 'npm.cmd' : 'npm', ['run',  "build"], { cwd: "/content/svelte" });

  // data seems to be encoded in UTF-8
  build.stdout.on('data', (data) => {
    res.write(data)
  })

  build.stderr.on('data', (data) => {
    res.write(data)
  })

  build.on('close', (code) => {
    res.end()
  })

})

app.listen(process.env.CONTENT_PORT)

