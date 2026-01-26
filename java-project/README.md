# Java Project

A simple Java project with Maven build system.

## Project Structure

```
java-project/
├── pom.xml                           # Maven configuration file
├── README.md                         # This file
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           └── Main.java     # Main application class
│   │   └── resources/                # Application resources
│   └── test/
│       ├── java/
│       │   └── com/
│       │       └── example/
│       │           └── MainTest.java # Test classes
│       └── resources/                # Test resources
```

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

## Building the Project

### Compile the project
```bash
mvn compile
```

### Run tests
```bash
mvn test
```

### Package the project
```bash
mvn package
```

### Run the application
```bash
mvn exec:java
```

Or if you want to run with arguments:
```bash
mvn exec:java -Dexec.args="arg1 arg2 arg3"
```

### Clean build artifacts
```bash
mvn clean
```

## Running the JAR file

After building with `mvn package`, you can run the JAR file directly:

```bash
java -cp target/java-project-1.0.0.jar com.example.Main
```

## Development

The main class is located at `src/main/java/com/example/Main.java`. You can modify this file to add your application logic.

Test classes should be placed in `src/test/java/com/example/` and follow the naming convention `*Test.java`.

## Dependencies

This project currently includes:
- JUnit 5 for testing

You can add more dependencies by editing the `pom.xml` file in the `<dependencies>` section.

