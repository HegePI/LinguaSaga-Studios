using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using TMPro;
public class CharacterMovement : MonoBehaviour
{
    private SpriteRenderer NPC1SpriteRenderer;
    public float speed = 5.0f;
    public float slopeMovement = 0f;
    bool slopeFlag = false;

    private List<string> items = new List<string>();

    public GameObject canvasObject;
    private Animator animator;


    public GameObject inventory;

    private void Start()
    {
        animator = GetComponent<Animator>();
        NPC1SpriteRenderer = GetComponent<SpriteRenderer>();
    }

    private void Update()
    {
        if(!canvasObject.activeSelf)
        {
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");

            Vector3 currentInputDirection = new Vector3(horizontal, vertical + slopeMovement, 0.0f);
            
            if(items.Count > 0){
                string text = "Inventory: ";
                foreach (var item in items)
                {
                    text += item;
                }
                inventory.GetComponent<TMP_Text>().text = text;
            }

            if (Input.GetAxisRaw("Horizontal") > 0)
            {
                NPC1SpriteRenderer.flipX = false;
                if (slopeFlag)
                {
                    slopeMovement = -1.0f;
                }
                
            }
            else if (Input.GetAxisRaw("Horizontal") < 0)
            {
                NPC1SpriteRenderer.flipX = true;
                if (slopeFlag)
                {
                    slopeMovement = 1.2f;
                }            
            }

            if (horizontal != 0 || vertical != 0)
            {
                //This "isMoving" detemines if the animation plays
                animator.SetBool("isMoving", true);

                //Actually move
                transform.Translate(currentInputDirection * speed * Time.deltaTime);
            }
            else
            {
                animator.SetBool("isMoving", false);
            }
        }
    }
    private void OnTriggerEnter2D(Collider2D Other)
    {
        if (Other.CompareTag("stairs"))
        {
            slopeFlag = true;
        }
        if (Other.CompareTag("gun"))
        {
            Other.gameObject.SetActive(false);
            items.Add("Gun");
        }
        
    }
    private void OnTriggerExit2D(Collider2D Other)
    {
        if (Other.CompareTag("stairs"))
        {
            slopeFlag = false;
            slopeMovement = 0.0f;
        }
    }
}
