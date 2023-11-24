using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using TMPro;
using UnityEngine.TextCore.Text;
using System;
using System.Threading;
using System.Net.WebSockets;
using System.Text;
using System.Threading.Tasks;

public class NPC2Behaviour : MonoBehaviour
{
    bool isInTriggerRange = false;
    public GameObject canvasObject;
    public GameObject canvasInteraction;
    public GameObject dialog;
    private ClientWebSocket websocket;
    private CancellationTokenSource cancellationTokenSource;
    public string message;
    bool initiateMission = false;
    
    public TMP_InputField input;

    async void Start()
    {
        
        //Initiate websocket for the NPC
/*         cancellationTokenSource = new CancellationTokenSource();
        websocket = new ClientWebSocket();
        

        try
        {
            await websocket.ConnectAsync(new Uri("ws://127.0.0.1:8000/ws/conversation/npc2"), cancellationTokenSource.Token);
            Debug.Log("WebSocket connected!");

            //Initiate function to receive messages from websocket
            _ = ReceiveMessages();
        }
        catch (Exception e)
        {
            Debug.LogError("WebSocket connection error: " + e.Message);
        } */
    }
    
    private void Update()
    {
        
        if (isInTriggerRange){
            canvasInteraction.SetActive(true);
        }
        else {
            canvasInteraction.SetActive(false);
        }
        if (Input.GetButtonDown("Interact") && isInTriggerRange)
        {
            canvasObject.SetActive(true);  

            input.onSubmit.AddListener(SendUserMessage);
        }
        else if (!isInTriggerRange || Input.GetButtonDown("Cancel")){
            canvasObject.SetActive(false);
        }
        if (initiateMission)
        {
            Debug.Log("The mission has started");
           
        }
        
    }

    private async void SendUserMessage(string arg0)
    {   try
        {
            input.Select();
            //Send the input in the JSON format, store as a string, then converted to JSON
            string jsonString = "{'player_name': 'player2','player_input':'" + input.text + "', 'npc_data': {'npc_name': 'Jane Doe','backstory': '','description': '','tasks': [{'description': ''}]}}";
            jsonString = jsonString.Replace('\'', '\"');
            JObject jsonObject = JObject.Parse(jsonString);

            //Function defined to send json
            await SendJsonAsync(jsonObject);
            
            
        }
        catch (Exception e)
        {
            Debug.LogError("WebSocket connection error: " + e.Message);
        }
    }

    //Sends JSON through the websocket
    private async Task SendJsonAsync(object data)
    {
        if (websocket.State != WebSocketState.Open)
        {
            Debug.LogError("WebSocket is not connected.");
            return;
        }

        string json = JsonConvert.SerializeObject(data);
        var encoded = Encoding.UTF8.GetBytes(json);
        var buffer = new ArraySegment<Byte>(encoded, 0, encoded.Length);
        await websocket.SendAsync(buffer, WebSocketMessageType.Text, true, cancellationTokenSource.Token);
    }

    private async Task ReceiveMessages()
    {
        var buffer = new byte[1024 * 4];

        while (websocket.State == WebSocketState.Open)
        {
            try
            {
                var result = await websocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationTokenSource.Token);
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    await websocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, cancellationTokenSource.Token);
                }
                else
                {
                    message = Encoding.UTF8.GetString(buffer, 0, result.Count);

                    //First check if it is a mission text
                    if (message.Contains("<MISSION_INITIATED>"))
                    {
                        initiateMission = true;
                        message = message.Replace("<MISSION_INITIATED>", "");
                    }
                    //Display message in canvas after receiving it from response
                    dialog.GetComponent<TMP_Text>().text = "\n\n" + message + dialog.GetComponent<TMP_Text>().text;
                    input.text = "";
                }
            }
            catch (Exception e)
            {
                Debug.LogError("Error in receiving WebSocket message: " + e.Message);
                break;
            }
        }
    }
    private void OnTriggerStay2D(Collider2D Other){
        isInTriggerRange = true;
    }
    private void OnTriggerExit2D(Collider2D Other){
        isInTriggerRange = false;
        
    }
}