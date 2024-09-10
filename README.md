### GPT-4o Photocritic

This is a simple [Chainlit](https://chainlit.io/) app to demonstrate the multi-modal capabilities of [GPT-4o](https://openai.com/index/hello-gpt-4o/).

It makes calls to GPT-4o through the [Github Models Marketplace](https://github.com/marketplace/models), currently in beta.

<video controls>
  <source src="assets/gpt-4o-photocritic.mp4" type="video/mp4">
</video>

### Usage

This application requires both the `chainlit` and `openai` python packages to be installed:
```bash
pip install chainlit openai
```

After installing, you will also need to have access to [Github models](https://github.com/marketplace/models) and create a [Github token](https://github.com/settings/tokens) and then add it as an environment variable using one of the commands below:
```bash
# Mac / Linux
export GITHUB_TOKEN="<your-github-token-goes-here>"

# Powershell (Windows)
$Env:GITHUB_TOKEN="<your-github-token-goes-here>"

# Command Prompt (Windows)
set GITHUB_TOKEN="<your-github-token-goes-here>"
```

Finally, you can run the application using:
```
chainlit run photocritic.py
```

If you'd prefer not to use Github marketplace, you can remove the `base_url` and `api_key` arguments in `photocritic.py` to fall back to using an OpenAI account (and incurring charges w GPT-4o(-mini)).

**Functionalities:**   
✅ Basic text input / output  
✅ Streaming  
✅ Image processing  
✅ Responses with images  
✅ Multi-image input  
❌ Custom engineered prompts  
❌ Update UI and customize  
❌ Tool use (search? image generation?)  