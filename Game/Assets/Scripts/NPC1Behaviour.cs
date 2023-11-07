using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using Newtonsoft.Json.Linq;
using TMPro;
using UnityEngine.TextCore.Text;
using System;

public class NPC1Behaviour : MonoBehaviour
{
    bool isInTriggerRange = false;
    public GameObject canvasObject;

    public GameObject dialog;

    public TMP_InputField input;

    
    private void Update()
    {
       
        if (Input.GetButtonDown("Interact") && isInTriggerRange)
        {
            canvasObject.SetActive(true);  
            input.onSubmit.AddListener(SendUserMessage);
        }

        if (!isInTriggerRange || Input.GetButtonDown("Cancel")){
            canvasObject.SetActive(false);
        }
    }

    private void SendUserMessage(string arg0)
    {
        dialog.GetComponent<TMP_Text>().text = input.text;
        input.text = "";
    }
    /*
    The API for a simple get request. To be updated later once we have full code. For now, let's just print something out with a function "NPC Response"
    IEnumerator FetchNPCResponse()
    {
        string url = "";
        using (UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();
            if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError(request.error);
            }
            else
            {
                string responseData = request.downloadHandler.text;
                JObject json = JObject.Parse(responseData);
                Debug.Log("Hi! My name is " + json["first_name"].ToString() + " " + json["last_name"].ToString());
            }
        }
        
    }
    */
    private void OnTriggerStay2D(Collider2D Other){
        isInTriggerRange = true;
    }
    private void OnTriggerExit2D(Collider2D Other){
        isInTriggerRange = false;
        
    }
}