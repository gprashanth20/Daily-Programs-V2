public class LinkedListReversal {
    static class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    static Node reverse(Node head) {
        Node prev = null;
        while (head != null) {
            Node next = head.next;
            head.next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }

    static void print(Node head) {
        StringBuilder sb = new StringBuilder();
        while (head != null) {
            sb.append(head.value).append(" -> ");
            head = head.next;
        }
        sb.append("null");
        System.out.println(sb);
    }

    public static void main(String[] args) {
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        print(head);
        head = reverse(head);
        print(head);
    }
}
