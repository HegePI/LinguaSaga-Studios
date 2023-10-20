using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterMovement : MonoBehaviour
{
    public float speed = 5.0f; // Movement speed
    private Animator animator; // Reference to the Animator component

    private void Start()
    {
        animator = GetComponent<Animator>();
    }

    private void Update()
    {
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");

        Vector3 movement = new Vector3(horizontal, vertical, 0.0f);
        
        if(movement != Vector3.zero)
        {
            animator.SetBool("isMoving", true); // Play your movement animation
            transform.Translate(movement * speed * Time.deltaTime);
        }
        else
        {
            animator.SetBool("isMoving", false); // Stop the movement animation or transition to an idle state
        }
    }

    void OnTriggerEnter(Collider objectName)
    {
        Debug.Log("Entered collision with " + objectName.gameObject.name);
    }
}