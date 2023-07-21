/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode h1 = l1, h2=l2;
        ListNode prev = null;
        
        int carry = 0;
        while(h1!= null && h2!=null){
             h1.val = h1.val + h2.val ;
             if(carry == 1){ // if carry exist, add carry
                 h1.val++;
                 carry = 0;
             }
             if(h1.val >= 10){ // if sum >= 10, generate carry and keep the remaining in then val
                 h1.val -= 10;
                 carry = 1;
             }

             prev = h1;
             h1 = h1.next;
             h2 = h2.next;
         }
        
        if(h2 != null){
            prev.next = h2; // if h2 is bigger, just join the remaining list
        }
        
        ListNode curr = (h1 == null)?h2:h1; // taking the bigger one
        
        while(carry != 0 && curr != null){
             curr.val++;
             carry = 0;
             if(curr.val >= 10){
                 curr.val -= 10;
                 carry = 1;
             }
            prev = curr;
            curr = curr.next;
        }
        
        if(curr == null && carry != 0) prev.next = new ListNode(1); 
        
        return l1;
    }
}