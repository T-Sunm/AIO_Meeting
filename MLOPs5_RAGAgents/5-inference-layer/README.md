# Dynamo Inference

## Step 0: If you not have CUDA toolkit, please follow the instructions:

### Step 0.1: Configure the repository:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey |sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
&& sudo apt-get update
```

### Step 0.2: Install the NVIDIA Container Toolkit packages:

```bash
sudo apt-get install -y nvidia-container-toolkit
```

### Step 0.3: Configure the container runtime by using the nvidia-ctk command:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

### Step 0.4: Restart the Docker daemon:

```bash
sudo systemctl restart docker
```

## Step 1: Clone git
```bash
git clone --branch v0.2.0 https://github.com/ai-dynamo/dynamo.git
```

## Step 2: Build etcd and nats service 
```bash
cd dynamo &&
docker compose -f deploy/docker-compose.yml up -d
```

## Step 3: Build Dynamo Image
```bash
./container/build.sh --framework vllm --build-arg VLLM_MAX_JOBS=number_cpu
```

with number_cpu is a number of cores which you want to allocate for process to build image faster

## Step 4: Run Dynamo container

```bash
docker run --gpus all -it --rm --network host --shm-size=10G --ulimit memlock=-1 --ulimit stack=67108864 --ulimit nofile=65536:65536 -w /workspace --cap-add CAP_SYS_PTRACE --ipc host dynamo-vllm:0.2.0
```

Note: you can use my image is nguyenpnx/dynamo-vllm:0.2.0

## Step 5: Run LLM model inside Dynamo container

### 5.1. Run with Aggregated serving
```bash
cd $DYNAMO_HOME/examples/llm
dynamo serve graphs.agg:Frontend -f ./configs/agg.yaml
```

### 5.2. Run with Aggregated serving with KV Routing
```bash
cd $DYNAMO_HOME/examples/llm
dynamo serve graphs.agg_router:Frontend -f ./configs/agg_router.yaml
```

### 5.3. Run Disaggregated serving
```bash
cd $DYNAMO_HOME/examples/llm
dynamo serve graphs.disagg:Frontend -f ./configs/disagg.yaml
```

### 5.4. Run with Disaggregated serving with KV Routing
```bash
cd $DYNAMO_HOME/examples/llm
dynamo serve graphs.disagg_router:Frontend -f ./configs/disagg_router.yaml
```

## 6. Test with python script in Local

```bash
cd demo && 
uv run predict.py
```

## 7. Some tips with you met error `Out of GPU memory`

Modify 2 config in Dynamo container at:
- `block-size: 32` # in configs/agg.yaml
- `engine_args.dtype = "float32"` # in utils/vllm.py
