package ds_binarytrees;

import java.util.ArrayList;

/**
 *
 * @author ogm2
 */
public class BSTNode<E extends Comparable<E>> extends TreeNode<E> {

    /**
     * The entry v stored on this node.
     */
    E v;

    /**
     * The number of duplicates of this entry. Value 1 means this entry has no
     * duplicates.
     */
    int counter;

    /**
     * The left child of this node.
     */
    BSTNode lc;

    /**
     * The right child of this node.
     */
    BSTNode rc;

    /**
     * *************
     */
    /* CONSTRUCTORS */
    /**
     * *************
     */
    /**
     * Constructs an empty node.
     */
    public BSTNode() {
        v = null;
        counter = 0;
        lc = null;
        rc = null;
    }

    /**
     * Constructs a node with a single entry.
     *
     * @param v the entry v
     */
    public BSTNode(E newValue) {
        v = newValue;
        counter = 1;
        lc = null;
        rc = null;
    }

    /**
     * ******************
     */
    /* GETTERS & SETTERS */
    /**
     * ******************
     */
    public E getValue() {
        return v;
    }

    public void setValue(E v) {
        this.v = v;
        counter = 1;
    }

    public int getCounter() {
        return counter;
    }

    public void setCounter(int counter) {
        this.counter = counter;
    }

    public BSTNode getLeftChild() {
        return lc;
    }

    public void setLeftChild(BSTNode lc) {
        this.lc = lc;
    }

    public BSTNode getRightChild() {
        return rc;
    }

    public void setRightChild(BSTNode rc) {
        this.rc = rc;
    }

    /**
     * ***********************************
     */
    /* SUBTREE EXPLORATION & MODIFICATION */
    /**
     * ***********************************
     */
    public void add(E newValue) {
        if (v.compareTo(newValue) == 0) {
            counter++;
        } else if (newValue.compareTo(v) < 0) {
            if (lc == null) {
                lc = new BSTNode(newValue);
            } else {
                lc.add(newValue);
            }
        } else {
            if (rc == null) {
                rc = new BSTNode(newValue);
            } else {
                rc.add(newValue);
            }
        }
    }

    /**
     * Replaces a child node with another node. If the replaced child is the
     * left (right) child then the new node becomes the left (right) child of
     * this node.
     *
     * @param oldNode
     * @param newNode
     */
    public void replaceChild(BSTNode oldNode, BSTNode newNode) {
        System.out.println("Replacing node " + oldNode.getValue());
        if (lc == oldNode) {
            lc = newNode;
        } else {
            rc = newNode;
        }
    }

    /**
     * Removes this node from the tree. If this node is a leaf, get parent to
     * replace this node with null. If this node has only one child, get parent
     * to replace this node with its child. If this node has two children, get
     * parent to replace this node with its successor (ie. the node that stores
     * the closest yet greater v in the tree), and remove successor from its
     * original place in the tree.
     *
     * @param parent the parent node of the current node
     */
    public void removeNode(BSTNode parent) {
        System.out.println("Removing " + this.getValue());
        if (this.isLeaf()) {
            parent.replaceChild(this, null);
        } else if (this.hasSingleChild()) {
            if (lc != null) {
                parent.replaceChild(this, lc);
            } else {
                parent.replaceChild(this, rc);
            }
        } else { //this node has two children
            //Find successor
            BSTNode successor = rc;
            BSTNode parentOfSuccessor = this;
            while (successor.getLeftChild() != null) {
                parentOfSuccessor = successor;
                successor = successor.getLeftChild();
            }
            //Remove successor
            parentOfSuccessor.replaceChild(successor, successor.getRightChild());
            //Update removed node v and counter with those of its successor
            this.counter = successor.getCounter();
            this.v = (E) successor.getValue();
        }
    }

    /**
     * Determines whether the node is a leaf.
     *
     * @return true if the node is a leaf, false otherwise
     */
    public boolean isLeaf() {
        return ((lc == null) && (rc == null));
    }

    /**
     * Determines whether the node has only one child.
     *
     * @return true if the node has only one child, false otherwise
     */
    public boolean hasSingleChild() {
        // Operator ^ is XOR, ie. one or the other but neither both nor none
        return ((lc == null) ^ (rc == null));
    }

    /**
     * Explores the subtree to find an entry.
     *
     * @param v the entry v to look for
     * @return the node that stores the v if the v appears in the
     * subtree, null otherwise
     */
    public BSTNode find(E v) {
        BSTNode result = null;
        if (v.compareTo(this.v) == 0) {
            result = this;
        } else if ((v.compareTo(this.v) < 0) && (lc != null)) {
            result = lc.find(v);
        } else if ((v.compareTo(this.v) > 0) && (rc != null)) {
            result = rc.find(v);
        }
        return result;
    }

    /**
     * Displays the subtree entries via a recursive in-order traversal.
     */
    public void displayInOrder() {
        if (lc != null) {
            lc.displayInOrder();
        }
        for (int i = 0; i < counter; i++) {
            System.out.print(v.toString() + " ");
        }
        if (rc != null) {
            rc.displayInOrder();
        }
    }

    /**
     * Displays the subtree entries via a recursive pre-order traversal.
     */
    public void displayPreOrder() {
        for (int i = 0; i < counter; i++) {
            System.out.print(v.toString() + " ");
        }
        if (lc != null) {
            lc.displayPreOrder();
        }
        if (rc != null) {
            rc.displayPreOrder();
        }
    }

    /**
     * Displays the subtree entries via a recursive post-order traversal.
     */
    public void displayPostOrder() {
        if (rc != null) {
            rc.displayPostOrder();
        }
        if (lc != null) {
            lc.displayPostOrder();
        }
        for (int i = 0; i < counter; i++) {
            System.out.print(v.toString() + " ");
        }
    }

    public int nbOfLeaves() {
        // TO DO
        int leaves = 0;
        if (this.v == null) {
            return 0;
        } else if (this.isLeaf()) {
            return 1;
        } else {
            if (this.lc != null && this.rc == null) {
                leaves = this.lc.nbOfLeaves();
            } else if (this.lc == null && this.rc != null) {
                leaves = this.rc.nbOfLeaves();
            } else {
                leaves = this.lc.nbOfLeaves() + this.rc.nbOfLeaves();
            }
        }
        return leaves;
    }
    /**
     * Computes the total number of nodes in this node's subtree.
     *
     * @return the total number of nodes in this node's subtree, 1 if this node
     * is a leaf
     */
    
    /**
     * Computes the total number of leaves in this node's subtree.
     *
     * @return the total number of leaves in this node's subtree
     */
    

    /**
     * Computes the height (number of levels) of this node's subtree.
     *
     * @return the height of this node's subtree
     */
    public int height() {
        // TO DO
        if (this.v == null) {
            return 0;
        }
        




            return 1;




        } else {
            if (this.lc != null && this.rc == null) {
                return (1 + this.lc.height());
            } else if (this.lc == null && this.rc != null) {
                return (1 + this.rc.height());
            } else {
                return (1 + Math.max(this.lc.height(), this.rc.height()));
            }
        }
    }

   
    public void getAllInRange(E min, E max, ArrayList<E> l) {
        // TO DO
        if (this.v.compareTo(max) <= 0 && this.v.compareTo(min) >= 0) {
            l.add(this.v);
            if (this.counter != 0) {
                for (int i = 0; i < this.counter - 1; i++) {
                    l.add(this.v);
                }
            }
        }
        if (this.lc != null) {
            this.lc.getAllInRange(min, max, l);
        }
        if (this.rc != null) {
            this.rc.getAllInRange(min, max, l);
        }
    }

    public void reverseTree() {
        // TO DO
        BSTNode temp = this.rc;
        this.rc = this.lc;
        this.lc = temp;
        if(this.lc != null){
            this.lc.reverseTree();
        }
        if(this.rc != null){
            this.rc.reverseTree();
        }
    }

    public int nbOfNodes() {
        // TO DO
        int num = 1;
        if (this.v == null) {
            return 0;
        }
        if (this.lc != null) {
            num += this.lc.nbOfNodes();
        }
        if (this.rc != null) {
            num += this.rc.nbOfNodes();
        }
        if (this.counter != 0) {
            for (int i = 0; i < this.counter - 1; i++) {
                num++;
            }
        }
        return num;
    }


}
