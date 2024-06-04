using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class ChatBot : MonoBehaviour
{
    public InputField userInputField;
    public Text chatOutputText;

    private string apiUrl = "http://localhost:5000/chat";

    public void SendMessageToBot()
    {
        string userMessage = userInputField.text;
        if (!string.IsNullOrEmpty(userMessage))
        {
            StartCoroutine(SendChatRequest(userMessage));
            userInputField.text = "";
        }
    }

    private IEnumerator SendChatRequest(string userMessage)
    {
        var jsonData = JsonUtility.ToJson(new { message = userMessage });
        var postData = System.Text.Encoding.UTF8.GetBytes(jsonData);

        UnityWebRequest request = new UnityWebRequest(apiUrl, "POST");
        request.uploadHandler = new UploadHandlerRaw(postData);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
        }
        else
        {
            var jsonResponse = request.downloadHandler.text;
            var chatResponse = JsonUtility.FromJson<ChatResponse>(jsonResponse);
            chatOutputText.text += "\nElara: " + chatResponse.response;
        }
    }
}

[System.Serializable]
public class ChatResponse
{
    public string response;
}
