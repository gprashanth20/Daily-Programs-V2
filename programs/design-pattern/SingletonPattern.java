public class SingletonPattern {
    private static volatile SingletonPattern instance;
    private int value;

    private SingletonPattern() {
        value = 0;
    }

    public static SingletonPattern getInstance() {
        if (instance == null) {
            synchronized (SingletonPattern.class) {
                if (instance == null) {
                    instance = new SingletonPattern();
                }
            }
        }
        return instance;
    }

    public void increment() { value++; }
    public int getValue() { return value; }

    public static void main(String[] args) {
        SingletonPattern a = SingletonPattern.getInstance();
        SingletonPattern b = SingletonPattern.getInstance();
        a.increment();
        b.increment();
        System.out.println("Shared value: " + a.getValue());
        System.out.println("Same instance: " + (a == b));
    }
}
