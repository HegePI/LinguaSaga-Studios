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

public class NPC1Behaviour : MonoBehaviour
{
    bool isInTriggerRange = false;
    public GameObject canvasObject;
    public GameObject canvasInteraction;
    public GameObject dialog;
    private ClientWebSocket websocket;
    private CancellationTokenSource cancellationTokenSource;
    public string message;
    public bool initiateMission = false;
    public TMP_InputField input;
    public GameObject gun;
    public GameObject tablet;
    public GameObject inventory;
    public GameObject guestList;
    async void Start()
    {
        gun.SetActive(false);
        tablet.SetActive(false);

        guestList.GetComponent<TMP_Text>().text = "Find someone to talk to";

        //Initiate websocket for the NPC
        cancellationTokenSource = new CancellationTokenSource();
        websocket = new ClientWebSocket();

        try
        {
            await websocket.ConnectAsync(new Uri("ws://127.0.0.1:8000/ws/conversation/npc1"), cancellationTokenSource.Token);
            Debug.Log("WebSocket connected!");

            //Initiate function to receive messages from websocket
            _ = ReceiveMessages();
        }
        catch (Exception e)
        {
            Debug.LogError("WebSocket connection error: " + e.Message);
        }
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
            if (inventory.GetComponent<TMP_Text>().text.Contains("Gun") && inventory.GetComponent<TMP_Text>().text.Contains("Tablet"))
            {
                SendUserMessage("Here, I got your stuff back");
                initiateMission = false;
                inventory.GetComponent<TMP_Text>().text = "";
                guestList.GetComponent<TMP_Text>().text = "All guests done";
            }
            else
            {
                input.onSubmit.AddListener(SendUserMessage);
            }
        }
        else if (!isInTriggerRange || Input.GetButtonDown("Cancel")){
            canvasObject.SetActive(false);
        }
        if (initiateMission)
        {
            print(inventory.GetComponent<TMP_Text>().text);
            if (inventory.GetComponent<TMP_Text>().text.Contains("Gun") && inventory.GetComponent<TMP_Text>().text.Contains("Tablet"))
            {
                guestList.GetComponent<TMP_Text>().text = "Deliver John's gun and tablet back";
            }
            else if(inventory.GetComponent<TMP_Text>().text.Contains("Gun"))
            {
                guestList.GetComponent<TMP_Text>().text = "Find John's Tablet";
            }
            else if(inventory.GetComponent<TMP_Text>().text.Contains("Tablet"))
            {
                guestList.GetComponent<TMP_Text>().text = "Find John's Gun";
            }
            else if (initiateMission)
            {
                guestList.GetComponent<TMP_Text>().text = "Find John's Gun And Tablet";
            }

        }
        
    }

    private async void SendUserMessage(string arg0)
    {   try
        {
            string finalInput = "";
            if (!inventory.GetComponent<TMP_Text>().text.Contains("gun") && !inventory.GetComponent<TMP_Text>().text.Contains("tablet"))
            {
                input.Select();
                finalInput = input.text;
            }
            else if (inventory.GetComponent<TMP_Text>().text.Contains("gun") && inventory.GetComponent<TMP_Text>().text.Contains("tablet"))
            {
                finalInput = arg0;
                inventory.GetComponent<TMP_Text>().text = "";
            }
            //Send the input in the JSON format, store as a string, then converted to JSON
            string jsonString = "{'player_name': 'player1','player_input':'" + finalInput + "', 'npc_data': {'npc_name': 'John Silverhand','backstory': '','description': '','tasks': [{'description': 'Fetch my gun and my tablet'}]}}";
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