abstract class Conta{
    private String titular;
    protected double saldo;
    // Construtor
    public Conta(String titular, double saldoInicial){
        this.titular = titular;
        this.saldo = saldoInicial;
    }
    public void depositar(double valor){
        if (valor > 0){
            saldo += valor;
            System.out.println("Depositado: R$ " + valor);
        }
    }
    public double getSaldo(){
        return saldo;
    }
    public abstract void sacar(double valor);

}


Class ContaPoupanca extends Conta {
    private double taxaRendimento = 0.05;
    protected double Rendimento = saldo * taxaRendimento;
    public ContaPoupanca(String titular, double saldoInicial){
        super (titular, saldoInicial)
    }
    @Override 
    public void sacar(double valor){
        if (valor <= saldo){
            System.out.println("Saque de R$: " + valor + "Realizar na Poupança");
        }else{
            System.out.println("Saldo Insuficiente!");
        }
    }
}

public class Main {
    public static void main(String[] args){
        Conta MinhaConta = new ContaPoupanca("Gustavo Henrique",1000.0);
        MinhaConta.depositar(500);
        MinhaConta.sacar(200);
        System.out.println("Valor na conta depois da transação: " + minhaConta.getSaldo());
    }
}
