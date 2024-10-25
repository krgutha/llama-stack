# Getting Started with Llama Stack

This guide will walk you though the steps to get started on end-to-end flow for LlamaStack. This guide mainly focuses on getting started with building a LlamaStack distribution, and starting up a LlamaStack server. Please see our [documentations](../README.md) on what you can do with Llama Stack, and [llama-stack-apps](https://github.com/meta-llama/llama-stack-apps/tree/main) on examples apps built with Llama Stack.

## Installation
The `llama` CLI tool helps you setup and use the Llama toolchain & agentic systems. It should be available on your path after installing the `llama-stack` package.

You have two ways to install this repository:

1. **Install as a package**:
   You can install the repository directly from [PyPI](https://pypi.org/project/llama-stack/) by running the following command:
   ```bash
   pip install llama-stack
   ```

2. **Install from source**:
   If you prefer to install from the source code, follow these steps:
   ```bash
    mkdir -p ~/local
    cd ~/local
    git clone git@github.com:meta-llama/llama-stack.git

    conda create -n stack python=3.10
    conda activate stack

    cd llama-stack
    $CONDA_PREFIX/bin/pip install -e .
   ```

For what you can do with the Llama CLI, please refer to [CLI Reference](./cli_reference.md).

## Starting Up Llama Stack Server

You have two ways to start up Llama stack server:

1. **Starting up server via docker**:

	We provide 2 pre-built Docker image of Llama Stack distribution, which can be found in the following links.
	- [llamastack-local-gpu](https://hub.docker.com/repository/docker/llamastack/llamastack-local-gpu/general)
	- This is a packaged version with our local meta-reference implementations, where you will be running inference locally with downloaded Llama model checkpoints.
	- [llamastack-local-cpu](https://hub.docker.com/repository/docker/llamastack/llamastack-local-cpu/general)
	- This is a lite version with remote inference where you can hook up to your favourite remote inference framework (e.g. ollama, fireworks, together, tgi) for running inference without GPU.

	> [!NOTE]
	> For GPU inference, you need to set these environment variables for specifying local directory containing your model checkpoints, and enable GPU inference to start running docker container.
	```
	export LLAMA_CHECKPOINT_DIR=~/.llama
	```

	> [!NOTE]
	> `~/.llama` should be the path containing downloaded weights of Llama models.

	To download llama models, use
	```
	llama download --model-id Llama3.1-8B-Instruct
	```

	To download and start running a pre-built docker container, you may use the following commands:

	```
	docker run -it -p 5000:5000 -v ~/.llama:/root/.llama --gpus=all llamastack/llamastack-local-gpu
	```

	> [!TIP]
	> Pro Tip: We may use `docker compose up` for starting up a distribution with remote providers (e.g. TGI) using [llamastack-local-cpu](https://hub.docker.com/repository/docker/llamastack/llamastack-local-cpu/general). You can checkout [these scripts](../distributions/) to help you get started.


2. **Build->Configure->Run Llama Stack server via conda**:

	You may also build a LlamaStack distribution from scratch, configure it, and start running the distribution. This is useful for developing on LlamaStack.

	**`llama stack build`**
	- You'll be prompted to enter build information interactively.
	```
	llama stack build

	> Enter an unique name for identifying your Llama Stack build distribution (e.g. my-local-stack): my-local-stack
	> Enter the image type you want your distribution to be built with (docker or conda): conda

	Llama Stack is composed of several APIs working together. Let's configure the providers (implementations) you want to use for these APIs.
	> Enter the API provider for the inference API: (default=meta-reference): meta-reference
	> Enter the API provider for the safety API: (default=meta-reference): meta-reference
	> Enter the API provider for the agents API: (default=meta-reference): meta-reference
	> Enter the API provider for the memory API: (default=meta-reference): meta-reference
	> Enter the API provider for the telemetry API: (default=meta-reference): meta-reference

	> (Optional) Enter a short description for your Llama Stack distribution:

	Build spec configuration saved at ~/.conda/envs/llamastack-my-local-stack/my-local-stack-build.yaml
	You can now run `llama stack configure my-local-stack`
	```

	**`llama stack configure`**
	- Run `llama stack configure <name>` with the name you have previously defined in `build` step.
	```
	llama stack configure <name>
	```
	- You will be prompted to enter configurations for your Llama Stack

	```
	$ llama stack configure my-local-stack

	Could not find my-local-stack. Trying conda build name instead...
	Configuring API `inference`...
	=== Configuring provider `meta-reference` for API inference...
	Enter value for model (default: Llama3.1-8B-Instruct) (required):
	Do you want to configure quantization? (y/n): n
	Enter value for torch_seed (optional):
	Enter value for max_seq_len (default: 4096) (required):
	Enter value for max_batch_size (default: 1) (required):

	Configuring API `safety`...
	=== Configuring provider `meta-reference` for API safety...
	Do you want to configure llama_guard_shield? (y/n): n
	Do you want to configure prompt_guard_shield? (y/n): n

	Configuring API `agents`...
	=== Configuring provider `meta-reference` for API agents...
	Enter `type` for persistence_store (options: redis, sqlite, postgres) (default: sqlite):

	Configuring SqliteKVStoreConfig:
	Enter value for namespace (optional):
	Enter value for db_path (default: /home/xiyan/.llama/runtime/kvstore.db) (required):

	Configuring API `memory`...
	=== Configuring provider `meta-reference` for API memory...
	> Please enter the supported memory bank type your provider has for memory: vector

	Configuring API `telemetry`...
	=== Configuring provider `meta-reference` for API telemetry...

	> YAML configuration has been written to ~/.llama/builds/conda/my-local-stack-run.yaml.
	You can now run `llama stack run my-local-stack --port PORT`
	```

	**`llama stack run`**
	- Run `llama stack run <name>` with the name you have previously defined.
	```
	llama stack run my-local-stack

	...
	> initializing model parallel with size 1
	> initializing ddp with size 1
	> initializing pipeline with size 1
	...
	Finished model load YES READY
	Serving POST /inference/chat_completion
	Serving POST /inference/completion
	Serving POST /inference/embeddings
	Serving POST /memory_banks/create
	Serving DELETE /memory_bank/documents/delete
	Serving DELETE /memory_banks/drop
	Serving GET /memory_bank/documents/get
	Serving GET /memory_banks/get
	Serving POST /memory_bank/insert
	Serving GET /memory_banks/list
	Serving POST /memory_bank/query
	Serving POST /memory_bank/update
	Serving POST /safety/run_shield
	Serving POST /agentic_system/create
	Serving POST /agentic_system/session/create
	Serving POST /agentic_system/turn/create
	Serving POST /agentic_system/delete
	Serving POST /agentic_system/session/delete
	Serving POST /agentic_system/session/get
	Serving POST /agentic_system/step/get
	Serving POST /agentic_system/turn/get
	Serving GET /telemetry/get_trace
	Serving POST /telemetry/log_event
	Listening on :::5000
	INFO:     Started server process [587053]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://[::]:5000 (Press CTRL+C to quit)
	```


## Testing with client
Once the server is setup, we can test it with a client to see the example outputs.
```
cd /path/to/llama-stack
conda activate <env>  # any environment containing the llama-stack pip package will work

python -m llama_stack.apis.inference.client localhost 5000
```

This will run the chat completion client and query the distribution’s `/inference/chat_completion` API.

Here is an example output:
```
User>hello world, write me a 2 sentence poem about the moon
Assistant> Here's a 2-sentence poem about the moon:

The moon glows softly in the midnight sky,
A beacon of wonder, as it passes by.
```

You may also send a POST request to the server:
```
curl http://localhost:5000/inference/chat_completion \
-H "Content-Type: application/json" \
-d '{
	"model": "Llama3.1-8B-Instruct",
	"messages": [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": "Write me a 2 sentence poem about the moon"}
	],
	"sampling_params": {"temperature": 0.7, "seed": 42, "max_tokens": 512}
}'

Output:
{'completion_message': {'role': 'assistant',
  'content': 'The moon glows softly in the midnight sky, \nA beacon of wonder, as it catches the eye.',
  'stop_reason': 'out_of_tokens',
  'tool_calls': []},
 'logprobs': null}

```


Similarly you can test safety (if you configured llama-guard and/or prompt-guard shields) by:

```
python -m llama_stack.apis.safety.client localhost 5000
```


Check out our client SDKs for connecting to Llama Stack server in your preferred language, you can choose from [python](https://github.com/meta-llama/llama-stack-client-python), [node](https://github.com/meta-llama/llama-stack-client-node), [swift](https://github.com/meta-llama/llama-stack-client-swift), and [kotlin](https://github.com/meta-llama/llama-stack-client-kotlin) programming languages to quickly build your applications.

You can find more example scripts with client SDKs to talk with the Llama Stack server in our [llama-stack-apps](https://github.com/meta-llama/llama-stack-apps/tree/main/examples) repo.


## Advanced Guides
Please see our [Building a LLama Stack Distribution](./building_distro.md) guide for more details on how to assemble your own Llama Stack Distribution.
