function graphics(x_col, y_col, graph_type) {
    const spawner = require('child_process').spawn;

    const data_to_pass_in = {'x_col':x_col, 'y_col':y_col, 'graph_type':graph_type};

    const graph_process = spawner('python', ['./testpy.py', JSON.stringify(data_to_pass_in)])
    
    graph_process.stdout.on('data', (data) => {
        console.log('Data Received from python script: ', data.toString());
    })
}

graphics("sex","age","scatter")