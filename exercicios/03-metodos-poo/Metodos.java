	public class Metodos{
	public static void main(String[] args){
		tabuada(9);

		if (verIdade(20)){
			System.out.println("É maior de idade.");
		}
		else{
			System.out.println("É menor de idade.");
		}

		System.out.println(somar(9,2));
	}

	public static boolean verIdade(int a){
		return a  >= 18;
	}

	public static int somar(int a, int b){
	return a + b;
	}
	
	public static void tabuada(int a){
		System.out.println("Tabuada do " + a + ".");
                for(int o = 1; o <= 10; o++){
                        	System.out.println(a + " * " + o + " = " + (a*o));
		}
		System.out.println("--------------------------");
	}
}
