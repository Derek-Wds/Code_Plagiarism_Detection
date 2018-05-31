import java.util.ArrayList;

/**
 * This class implements a Stack using two different implementations.
 * Stack is used with a regular array and Stack2 uses an ArrayList.
 *
 * A stack is exactly what it sounds like. An element gets added to the top of
 * the stack and only the element on the top may be removed. This is an example
 * of an array implementation of a Stack. So an element can only be added/removed
 * from the end of the array. In theory stack have no fixed size, but with an
 * array implementation it does.
 *
 * @author Unknown
 *
 */
class Stack{
	/** The max size of the Stack */
	private int maxSize;
	/** The array representation of the Stack */
	private int[] stackArray;
	/** The top of the stack */
	private int top;

	/**
	 * Constructor
	 *
	 * @param size Size of the Stack
	 */
	public Stack(int size){
		maxSize = size;
		stackArray = new int[maxSize];
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
			stackArray[top] = value;
		}else{
			resize(maxSize*2);
                        push(value);// don't forget push after resizing
		}
	}

	/**
	 * Removes the top element of the stack and returns the value you've removed
	 *
	 * @return value popped off the Stack
	 */
	public int pop(){
		if(!isEmpty()){ //Checks for an empty stack
			return stackArray[top--];
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
			return stackArray[top];
		}else{
			System.out.println("The stack is empty, cant peek");
			return -1;
		}
	}

	private void resize(int newSize){
		//private int[] transferArray = new int[newSize]; we can't put modifires here !
                int[] transferArray = new int[newSize];

		//for(int i = 0; i < stackArray.length(); i++){ the length isn't a method .
                for(int i = 0; i < stackArray.length; i++){
			transferArray[i] = stackArray[i];
			stackArray = transferArray;
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
	 * Deletes everything in the Stack
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
 * This is an ArrayList Implementation of stack, Where size is not
 * a problem we can extend the stack as much as we want.
 *
 * @author Unknown
 *
 */
class Stack2{
		/** ArrayList representation of the stack */
		ArrayList<Integer> stackList;

		/**
		 * Constructor
		 */
		Stack2(){
			stackList=new ArrayList<>();
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
		 * the top for Stack
		 *
		 * @return Element popped
		 */
		int pop(){

			if(!isEmpty()){ // checks for an empty Stack

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
		 * Checks for empty Stack
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

/**
 * This class implements the Stack and Stack2 created above
 *
 * @author Unknown
 *
 */
public class Stacks{
	/**
	 * Main method
	 *
	 * @param args Command line arguments
	 */
	public static void main(String args[]){
			Stack myStack = new Stack(4); //Declare a stack of maximum size 4
 		//Populate the stack
 		myStack.push(5);
 		myStack.push(8);
  		myStack.push(2);
  		myStack.push(9);

		System.out.println("*********************Stack Array Implementation*********************");
  		System.out.println(myStack.isEmpty()); //will print false
  		System.out.println(myStack.isFull()); //will print true
  		System.out.println(myStack.peek()); //will print 9
  		System.out.println(myStack.pop()); //will print 9
  		System.out.println(myStack.peek()); // will print 2

		Stack2 myStack2 = new Stack2(); //Declare a stack of maximum size 4
  		//Populate the stack
 		myStack2.push(5);
		myStack2.push(8);
 		myStack2.push(2);
 		myStack2.push(9);

 		System.out.println("*********************Stack List Implementation*********************");
 		System.out.println(myStack2.isEmpty()); //will print false
 		System.out.println(myStack2.peek()); //will print 9
 		System.out.println(myStack2.pop()); //will print 9
 		System.out.println(myStack2.peek()); // will print 2
 		System.out.println(myStack2.pop()); //will print 2
	}
}

/**
* Matrix data-type.
*
* @author Kyler Smith, 2017
*/


public class Matrix {

	public static void main(String[] args) {

		int[][] data1 = new int[0][0];
        int[][] data2 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        int[][] data3 = {{1, 4, 7}, {2, 5, 8}, {3, 6, 9}};

        Matrix m1 = new Matrix(data1);
        Matrix m2 = new Matrix(data2);
        Matrix m3 = new Matrix(data3);

        System.out.println("m1 --> Rows: " + m1.getRows() + " Columns: " + m1.getColumns());
        System.out.println("m2 --> Rows: " + m2.getRows() + " Columns: " + m2.getColumns());
        System.out.println("m3 --> Rows: " + m3.getRows() + " Columns: " + m3.getColumns());

        //check for reference issues
        System.out.println("m2 -->\n" + m2);
        data2[1][1] = 101;
        System.out.println("m2 -->\n" + m2);

        //test equals
        System.out.println("m2==null: " + m2.equals(null));             //false
        System.out.println("m3==\"MATRIX\": " + m2.equals("MATRIX"));   //false
        System.out.println("m2==m1: " + m2.equals(m1));                 //false
        System.out.println("m2==m2: " + m2.equals(m2));                 //true
        System.out.println("m2==m3: " + m2.equals(m3));                 //false

        //test operations (valid)
        System.out.println("2 * m2:\n" + m2.scale(2));
        System.out.println("m2 / 2:\n" + m2.divide(2));
        System.out.println("m2 + m3:\n" + m2.plus(m3));
        System.out.println("m2 - m3:\n" + m2.minus(m3));
        System.out.println("m2 * m3: \n"+m2.multiply(m3));
	}


    /**
     *  Data needs to be a deep copy as not to change the original state.
     */
    private int[][] data;

    /**
    * Constructor for the matrix takes in a 2D array
    *
    * @param pData
    */
    public Matrix(int[][] pData) {

        /** Make a deep copy of the data */
        if(pData.length != 0) {
            int[][] newData = new int[pData.length][pData[0].length];

            for(int i = 0; i < pData.length; i++)
                for(int j = 0; j < pData[0].length; j++)
                    newData[i][j] = pData[i][j];

            this.data = newData;
        } else {
            this.data = null;
        }
    }

    /**
    * Returns the element specified by the given location
    *
    * @param x : x cooridinate
    * @param y : y cooridinate
    * @return int : value at location
    */
    public int getElement(int x, int y) {
        return data[x][y];
    }

    /**
    * Returns the number of rows in the Matrix
    *
    * @return rows
    */
    public int getRows() {
    	if(this.data == null)
    		return 0;

        return data.length;
    }

    /**
    * Returns the number of rows in the Matrix
    *
    * @return columns
    */
    public int getColumns() {
    	if(this.data == null)
    		return 0;
        return data[0].length;
    }

    /**
	* Returns this matrix scaled by a factor. That is, computes sA where s is a
	* constant and A is a matrix (this object).
	*
	* @param scalar : value to scale by
	* @return A new matrix scaled by the scalar value
	*/
    public Matrix scale(int scalar) {

    	int[][] newData = new int[this.data.length][this.data[0].length];

		for (int i = 0; i < this.getRows(); ++i)
			for(int j = 0; j < this.getColumns(); ++j)
				newData[i][j] = this.data[i][j] * scalar;

		return new Matrix(newData);
    }
    
    /**
	* Returns this matrix divided by a factor. That is, computes sA where s is a
	* constant and A is a matrix (this object).
	*
	* @param scalar : value to divide by
	* @return A new matrix scaled by the scalar value
	*/
    public Matrix divide(int scalar) {

    	int[][] newData = new int[this.data.length][this.data[0].length];

		for (int i = 0; i < this.getRows(); ++i)
			for(int j = 0; j < this.getColumns(); ++j)
				newData[i][j] = this.data[i][j] / scalar;

		return new Matrix(newData);
    }

    /**
    * Adds this matrix to another matrix.
    *
    * @param other : Matrix to be added
    * @return addend
    */
    public Matrix plus(Matrix other) throws RuntimeException {

    	int[][] newData = new int[this.data.length][this.data[0].length];

    	if(this.getRows() != other.getRows() || this.getColumns() != other.getColumns())
			throw new RuntimeException("Not the same size matrix.");

    	for (int i = 0; i < this.getRows(); ++i)
			for(int j = 0; j < this.getColumns(); ++j)
				newData[i][j] = this.data[i][j] + other.getElement(i, j);

        return new Matrix(newData);
    }

    /**
    * Subtracts this matrix from another matrix.
    *
    * @param other : Matrix to be subtracted
    * @return difference
    */
    public Matrix minus(Matrix other) throws RuntimeException {

    	int[][] newData = new int[this.data.length][this.data[0].length];

    	if(this.getRows() != other.getRows() || this.getColumns() != other.getColumns())
			throw new RuntimeException("Not the same size matrix.");

    	for (int i = 0; i < this.getRows(); ++i)
			for(int j = 0; j < this.getColumns(); ++j)
				newData[i][j] = this.data[i][j] - other.getElement(i, j);

        return new Matrix(newData);
    }
    
    /**
     * Multiplies this matrix with another matrix.
     *
     * @param other : Matrix to be multiplied with
     * @return product
     */
     public Matrix multiply(Matrix other) throws RuntimeException {

     	int[][] newData = new int[this.data.length][other.getColumns()];

     	if(this.getColumns() !=other.getRows())
 			throw new RuntimeException("The two matrices cannot be multiplied.");
     	int sum;
     	for (int i = 0; i < this.getRows(); ++i)
 			for(int j = 0; j < other.getColumns(); ++j){
 				sum = 0;
 				for(int k=0;k<this.getColumns();++k){
 					sum += this.data[i][k] * other.getElement(k, j);
 				}
 				newData[i][j] = sum; 
 			}
 				

         return new Matrix(newData);
     }

    /**
    * Checks if the matrix passed is equal to this matrix
    *
	* @param other : the other matrix
	* @return boolean
    */
    public boolean equals(Matrix other) {
        return this == other;
    }

    /**
    * Returns the Matrix as a String in the following format
    *
    * [ a b c ] ...
    * [ x y z ] ...
    * [ i j k ] ...
    *    ...
    *
    * @return Matrix as String
	* TODO: Work formatting for different digit sizes
    */
    public String toString() {
        String str = "";

        for(int i = 0; i < this.data.length; i++) {
        	str += "[ ";
            for(int j = 0; j < this.data[0].length; j++) {
            	str += data[i][j];
            	str += " ";
            }
            str += "]";
            str += "\n";
        }

        return str;
    }
	
	/**
    * Returns transposed matrix of this matrix.
    *
    * @return transposed Matrix. 
    */
	public Matrix transpose() {
		
		int[][] newData = new int[this.data[0].length][this.data.length];

		for (int i = 0; i < this.getColumns(); ++i)
			for(int j = 0; j < this.getRows(); ++j)
				newData[i][j] = this.data[j][i];

		return new Matrix(newData);
	}		
}
