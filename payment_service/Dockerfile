FROM maven:3.8.1-openjdk-17-slim AS builder
WORKDIR ./
COPY pom.xml .
RUN mvn -e -B dependency:resolve
COPY src ./src
RUN mvn clean -DskipTests -e -B package

FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp
COPY --from=builder /target/*.jar /app.jar
ENTRYPOINT ["java","-jar","/app.jar"]