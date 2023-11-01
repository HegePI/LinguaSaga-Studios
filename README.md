# LinugaSaga Studios

LinugaSaga studios is a 2D game set in a dystopian synthwave universe. It attempts to use [LangChain](https://www.langchain.com/) framework along with [BLOOM](https://huggingface.co/bigscience/bloom) to create interactive converstation between characters.

The project structure along with a base description is given below.

```
LinugaSaga-Studios
├── Game                =====================> Contains game's base files. This folder can be imported in Unity
│   ├── Assembly-CSharp.csproj
│   ├── Assets
│   ├── Game.sln
│   ├── Library
│   ├── Logs
│   ├── Packages
│   ├── ProjectSettings
│   ├── README.md
│   ├── Temp
│   └── UserSettings
├── LanguageModel       =====================> Contains API facilitator and the core LLM models in Langchain framework
│   └── middleman       =====================> Contains the middleman (API facilitator)
│       └── model       =====================> Contains a wrapper for LangChain and BLOOM
├── LICENSE
└── README.md
```

Documentation on functionality and setting up of each module can be found in their respective folders. 

On a broad scale, the Game (made with [Unity](https://unity.com/)) has multiple non-playable characters (NPCs) which the player can interact with. The responses for each of the characters is sent and received via API calls. The middleman helps in facilitating the API calls between the game engine and the LLM models. The models folder contains a high-level abstraction UI for both LangChain and BLOOM which when initiated, starts a chat-like interface where we can input data for the LLM model to set the NPC context.