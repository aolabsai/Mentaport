
// Mentaport/api_snippets.ts


// configure agents with the number of inputs and outputs required -- run only once to build the config, then spawn agents
const set_agent_arch = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      'X-API-KEY': 'weBuildBottomUpAGIsForAll'
    },
    body: JSON.stringify({
      arch: {arch_i: '[10, 10, 10]', arch_z: '[5]', connector_function: 'full_conn'},
      kennel_name: 'TEST-Mentaport',
      email: 'mariale@mentaport.com',
      description: 'a 30-5 neuron agent, test configuration',
      permissions: 'open'
    })
  };
  
  fetch('https://api.aolabs.ai/prod/kennel', set_agent_arch)
    .then(res => res.json())
    .then(res => console.log(res))
    .catch(err => console.error(err));


    
    
// TRAIN AGENTS
const train_agent = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      'X-API-KEY': 'weBuildBottomUpAGIsForAll'
    },
    body: JSON.stringify({
        kennel_id: 'TEST-Mentaport',
        agent_id: 'scanner_01',  // change the ID here to provision distinct agents for each scanner
        email: 'mariale@mentaport.com',
        INPUT: '000000001100000001110000001010',  // this is dummy input!
        LABEL: '00000', // this is a dummy label!,-
        control: {
          US: true,
          states: 1
        }
    })
  };
  
  fetch('https://api.aolabs.ai/prod/kennel/agent', train_agent)
    .then(res => res.json())
    .then(res => console.log(res))
    .catch(err => console.error(err));




// TEST AGENTS
const test_agent = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      'X-API-KEY': 'weBuildBottomUpAGIsForAll'
    },
    body: JSON.stringify({
        kennel_id: 'TEST-Mentaport',
        agent_id: 'scanner_01',  // change the ID here to provision distinct agents for each scanner
        email: 'mariale@mentaport.com',
        INPUT: '000000001100000001110000001010',  // this is dummy input!
        control: {
          US: true,
          states: 3
        }
    })
  };
  
  fetch('https://api.aolabs.ai/prod/kennel/agent', test_agent)
    .then(res => res.json())
    .then(res => console.log(res))
    .catch(err => console.error(err));