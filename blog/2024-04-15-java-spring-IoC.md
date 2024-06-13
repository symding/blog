---
title: Spring IoC
tags: [java,spring]
---

> Inversion of Control 或简称 IoC 是一个对象不用 new 创建它就能定义其依赖关系的过程。对象将创建依赖关系的任务交给了 IoC 容器。
<!--truncate-->

## 核心概念
### Bean
Spring beans 是那些形成Spring应用的主干的java对象。它们被Spring IOC容器初始化，装配，和管理。
参考文章:
* [Spring Bean 定义](https://www.knowledgedict.com/tutorial/spring_framework-bean-definition.html)

## Demo
```java
// src/main/java/com/easyya/springstudy/studybean/domain/Person.java
import lombok.Data;

@Data
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void init() {
        System.out.println("a person initialized.");
    }

    public void destroy() {
        System.out.println("a person destroyed.");
    }
}

// src/main/java/com/easyya/springstudy/studybean/domain/man.java
import lombok.Data;

@Data
@Component
// @Component 注解在一个类上，表明将此类标记为Spring 容器中的一个Bean
// 而@Bean是针对方法的
public class Man {
    @Autowired
    @Qualifier("lisi")
    private Person person;

    public Man(Person p) {
        this.person = p;
    }

    public Person getPerson() {
        return this.person;
    }

    @Bean(initMethod = "init", destroyMethod = "destroy")
    public Person sunwukong1() {
        System.out.println("Init [假孙悟空]");
        return new Person("假的孙悟空", 500);
    }
}

// src/main/java/com/easyya/springstudy/config/PeopleConfig.java
import com.easyya.springstudy.studybean.domain.Address;
import com.easyya.springstudy.studybean.domain.Company;

// @Configuration注解中的bean方法仅会调用一次
// @Component注解中的方法每次都会调用
@Configuration
@ComponentScan(basePackageClasses = Man.class)
public class PeopleConfig {

    // @Bean 产生一个bean对象，然后将对象交给Spring管理
    // 产生这个Bean对象的方法Spring只会调用一次
    // 随后这个Spring将会将这个Bean对象放在自己的IOC容器中
    @Bean(initMethod = "init", destroyMethod = "destroy", name = "zhangsan")
    // @primary注解用来标志，当出现bean冲突时，优先使用哪个bean
    // 张三和李四都是Person类当使用@Autowired装配时会出现冲突
    // @primary 指示 优先使用张三
    @Primary
    public Person zhangSan() {
        System.out.println("Init [张三]");
        return new Person("李四", 25);
    }

    @Bean(initMethod = "init", destroyMethod = "destroy", name = "lisi")
    public Person liSi() {
        System.out.println("Init [李四]");
        return new Person("李四", 28);
    }

    @Bean(initMethod = "init", destroyMethod = "destroy")
    public Person wangwu() {
        System.out.println("Init [王五]");
        return new Person("王五", 38);
    }
}

// src/main/java/com/easyya/springstudy/controller/HelloBean.java
import com.easyya.springstudy.config.DomainConfig;

@Controller
public class HelloBean {
    // @Autowired 可以对类成员变量、方法及构造函数进行标注，完成自动装配的工作
    // 通过 @Autowired的使用来消除 set ，get方法
    // 通过 @Autowired 获取之前使用@Bean对该对象设置的实例
    @Autowired
    Person person1;

    @Autowired
    @Qualifier("lisi")
    Person person2;

    @Resource
    Person wangwu;

    @Resource
    Person sunwukong;

    @Autowired
    PeopleConfig pc;

    @Autowired
    Man c;

    @RequestMapping(value = "/hello_zhangsan", method = RequestMethod.GET)
    @ResponseBody
    public String HelloZhangSan() {
        return String.format("My name is %s, %d years old.", person1.getName(), person1.getAge());
    }

    @RequestMapping(value = "/hello_lisi", method = RequestMethod.GET)
    @ResponseBody
    public String HelloLiSi() {
        return String.format("My name is %s, %d years old.", person2.getName(), person2.getAge());
    }

    @RequestMapping(value = "/who_are_you", method = RequestMethod.GET)
    @ResponseBody
    public String Who() {
        Person p = c.getPerson();
        return String.format("My name is %s, %d years old.", p.getName(), p.getAge());
    }

    @RequestMapping(value = "/hello_wukong_fake", method = RequestMethod.GET)
    @ResponseBody
    public String HelloWuKong() {
        Person p = c.sunwukong1();
        return String.format("My name is %s, %d years old.", p.getName(), p.getAge());
    }

    @RequestMapping(value = "/hello_wukong", method = RequestMethod.GET)
    @ResponseBody
    public String HelloWuKong2() {
        Person p = pc.sunwukong();
        return String.format("My name is %s, %d years old.", p.getName(), p.getAge());
    }
}
```
`Spring` 在初始化时直接生成了 `Person zhangsan` `Person lisi` 两个 `Bean`，这两个 `Bean` 全部由 `Spring IoC` 管理，业务代码需要使用 `Person` 类时，无需使用 `new Person()` 方法创建或是使用函数传值方法引用，直接使用 `@Autowired` 注解引用 `IoC` 管理的 `Bean` 即可，可通过 `@Qualifier` `@Resource` 注解来指定要装配的 `Bean` (找到多个符合类型的 `Bean` 的情况下)。

### Test
```sh
curl http://127.0.0.1:8080/hello_zhangsan   # My name is 张三, 25 years old.
curl http://127.0.0.1:8080/hello_lisi       # My name is 李四, 28 years old.
curl http://127.0.0.1:8080/who_are_you      # My name is 李四, 28 years old.
```

```sh
curl http://127.0.0.1:8080/hello_wukong_fake    # My name is 假的孙悟空, 500 years old.
curl http://127.0.0.1:8080/hello_wukong_fake    # My name is 假的孙悟空, 500 years old.
curl http://127.0.0.1:8080/hello_wukong          # My name is 假的孙悟空, 500 years old.
curl http://127.0.0.1:8080/hello_wukong          # My name is 孙悟空, 500 years old.
```
::: info
Init [假孙悟空]
Init [假孙悟空]
:::
 `/hello_wukong_fake` 调用的是 `man` 中的 `sunwukong1` bean，但是 `Man` 的注解为 `@Componet`，所以每次调用都会重新生成，`/hello_wukong` 调用的是由 `@Configuration` 注解的 `Bean`，所以只会在初始化时生成一次。