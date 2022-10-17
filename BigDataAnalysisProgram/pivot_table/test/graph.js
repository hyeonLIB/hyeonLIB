// import {PythonShell} from
// 'python-shell';

// PythonShell.run(
//     'graph.py',
//     null,
//     function (err) {
//         if (err) throw err ;
//         console.log('finished');
//     }
// );


// import {PythonShell} from '/python-shell';

// PythonShell.runString('x=1+1;print(x)', null, function (err) {
//   if (err) throw err;
//   console.log('finished');
// });



// import {PythonShell} from 'python-shell';

// PythonShell.run('my_script.py', null, function (err) {
//   if (err) throw err;
//   console.log('finished');
// });
let {PythonShell} = require('python-shell')


import {PythonShell} from 'python-shell';

let options = {
  mode: 'text',
  pythonPath: 'path/to/python',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: 'path/to/my/scripts',
  args: ['value1', 'value2', 'value3']
};

PythonShell.run('my_script.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});