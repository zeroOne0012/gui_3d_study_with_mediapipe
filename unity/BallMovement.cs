using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallMovement : MonoBehaviour
{
    // Start is called before the first frame update

    public UDPReceive udpReceive;

    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        string data = udpReceive.data;
        data = data.Remove(0, 1); // 0부터 1개
        data = data.Remove(data.Length-1, 1); // 수신받은 좌표의 문자열인 '(x,y,z)' 문자열에서 괄호 제거
        // data.Length-2??
        //(255,361,50012) (x,y,area)
        string[] info = data.Split(','); // info = ['x', 'y', 'z']

        float x = float.Parse(info[0])/100; // string->float, 유니티의 좌표계의 규모에 맞게 조정
        float y = float.Parse(info[1])/100;
        float z = float.Parse(info[2])/1000;

        gameObject.transform.localPosition = new Vector3(x,y,z);
    }
}
