using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterMovement : MonoBehaviour
{

    //Attempt to implement basic collision? I dont know if this is optimal
    private Vector3 lastInputDirection = Vector3.zero;
    private bool canMove = true;
    

    public float speed = 5.0f;
    private Animator animator;

    private void Start()
    {
        animator = GetComponent<Animator>();
    }

    private void Update()
    {
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");

        Vector3 currentInputDirection = new Vector3(horizontal, vertical, 0.0f);

        //This is definitely not optimal
        if (currentInputDirection != Vector3.zero && lastInputDirection != currentInputDirection)
        {
            canMove = true;
        }

        //Stored for collision check. Basically, if you have collided, dont move, unless the direction is different. I can already see logical issues with this, but this is a primitive implmentation
        lastInputDirection = currentInputDirection;

        if (canMove)
        {
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
        else
        {
            animator.SetBool("isMoving", false);
        }
    }

    //This is broken and as basic as it can get
    private void OnTriggerEnter2D(Collider2D player)
    {
        canMove = false;
    }

}
