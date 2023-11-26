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
    public GameObject canvasObject;
    private Animator animator;
    public GameObject inventoryManagerGameObject;
    private InventoryManager inventory;


    private void Start()
    {
        animator = GetComponent<Animator>();
        NPC1SpriteRenderer = GetComponent<SpriteRenderer>();
        inventory = inventoryManagerGameObject.GetComponent<InventoryManager>();
        inventory.GetComponent<TMP_Text>().text = inventory.objectiveText;
    }

    private void Update()
    {
        if(!canvasObject.activeSelf)
        {
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");
            Vector3 currentInputDirection = new Vector3(horizontal, vertical + slopeMovement, 0.0f);

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
            inventory.itemPicked = true;
            if (inventory.itemPicked)
                inventory.GetComponent<TMP_Text>().text += "\nGun";
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
