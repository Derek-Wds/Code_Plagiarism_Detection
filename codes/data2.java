import java.util.arrList;

/**
 * This class implements a stk using two different implementations.
 * stk is used with a regular array and stk2 uses an arrList.
 *
 * A stack is exactly what it sounds like. An element gets added to the top of
 * the stack and only the element on the top may be removed. This is an example
 * of an array implementation of a stk. So an element can only be added/removed
 * from the end of the array. In theory stack have no fixed size, but with an
 * array implementation it does.
 *
 * @author Unknown
 *
 */
class stk{
	/** The max size of the stk */
	private int maxSize;
	/** The array representation of the stk */
	private int[] stackarr;
	/** The top of the stack */
	private int top;

	/**
	 * Constructor
	 *
	 * @param size Size of the stk
	 */
	public stk(int size){
		maxSize = size;
		stackarr = new int[maxSize];
		top = -1;
	}

	/**
	 * Adds an element to the top of the stack
	 *
	 * @param value The element added
	 */
	public void push(int value){
		if(!isFull()){ //Checks for a full stack
			top++;
			stackarr[top] = value;
		}else{
			resize(maxSize*2);
                        push(value);// don't forget push after resizing
		}
	}

	/**
	 * Removes the top element of the stack and returns the value you've removed
	 *
	 * @return value popped off the stk
	 */
	public int pop(){
		if(!isEmpty()){ //Checks for an empty stack
			return stackarr[top--];
		}

		if(top < maxSize/4){
			resize(maxSize/2);
			return pop();// don't forget pop after resizing
		}
		else{
			System.out.println("The stack is already empty");
			return -1;
		}
	}

	/**
	 * Returns the element at the top of the stack
	 *
	 * @return element at the top of the stack
	 */
	public int peek(){
		if(!isEmpty()){ //Checks for an empty stack
			return stackarr[top];
		}else{
			System.out.println("The stack is empty, cant peek");
			return -1;
		}
	}

	private void resize(int newSize){
		//private int[] transferarr = new int[newSize]; we can't put modifires here !
                int[] transferarr = new int[newSize];

		//for(int i = 0; i < stackarr.length(); i++){ the length isn't a method .
                for(int i = 0; i < stackarr.length; i++){
			transferarr[i] = stackarr[i];
			stackarr = transferarr;
		}
		maxSize = newSize;
	}

	/**
	 * Returns true if the stack is empty
	 *
	 * @return true if the stack is empty
	 */
	public boolean isEmpty(){
		return(top == -1);
	}

	/**
	 * Returns true if the stack is full
	 *
	 * @return true if the stack is full
	 */
	public boolean isFull(){
		return(top+1 == maxSize);
	}

	/**
	 * Deletes everything in the stk
	 *
	 * Doesn't delete elements in the array
	 * but if you call push method after calling
	 * makeEmpty it will overwrite previous
	 * values
	 */
	public void makeEmpty(){ //Doesn't delete elements in the array but if you call
		top = -1;			 //push method after calling makeEmpty it will overwrite previous values
	}
}

/**
 * This is an arrList Implementation of stack, Where size is not
 * a problem we can extend the stack as much as we want.
 *
 * @author Unknown
 *
 */
class stk2{
		/** arrList representation of the stack */
		arrList<Integer> stackList;

		/**
		 * Constructor
		 */
		stk2(){
			stackList=new arrList<>();
		}

		/**
		 * Adds value to the end of list which
		 * is the top for stack
		 *
		 * @param value value to be added
		 */
		void push(int value){
			stackList.add(value);
		}

		/**
		 * Pops last element of list which is indeed
		 * the top for stk
		 *
		 * @return Element popped
		 */
		int pop(){

			if(!isEmpty()){ // checks for an empty stk

				int popValue=stackList.get(stackList.size()-1);
				stackList.remove(stackList.size()-1);  //removes the poped element from the list
				return popValue;
			}
			else{
				System.out.print("The stack is already empty  ");
				return -1;
			}

		}

		/**
		 * Checks for empty stk
		 *
		 * @return true if stack is empty
		 */
		boolean isEmpty(){
			if(stackList.isEmpty())
				return true;

			else return false;

		}

		/**
		 * Top element of stack
		 *
		 * @return top element of stack
		 */
		int peek(){
			return stackList.get(stackList.size()-1);
		}
	}
