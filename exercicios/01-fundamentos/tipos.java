public class tipos {
	public static void main(String[] args) {
		int inteiro = 7;
		int outro = 2;

		System.out.println(inteiro / outro);
		System.out.println(inteiro % outro);
		System.out.println((double) inteiro / outro);

		double preco = 19.99;
		int precoInteiro = (int) preco;
		System.out.println(precoInteiro);

		String nome = "Leonardo";
		System.out.println("Ola " + nome + ", tens " + 25 + " anos");
	}
}
