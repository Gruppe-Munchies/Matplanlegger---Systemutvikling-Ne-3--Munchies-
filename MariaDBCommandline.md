
## Connecting to the MariaDB server with a username and password

The following command connects to the MariaDB server on the `localhost`:

```
mysql -u [username] -p[password]
Code language: SQL (Structured Query Language) (sql)
```

In this command:

`-u` specifies the username  
`-p` specifies the password of the username

Note that the password is followed immediately after the `-p` option.

For example, this command connects to the MariaDB server on the localhost:

```
mysql -u root -pS@cure1Pass
Code language: SQL (Structured Query Language) (sql)
```

In this command, `root` is the username and `S@cure1Pass` is the password of the `root` user account.

Notice that using the password on the command-line can be insecure. Typically, you leave out the password from the command as follows:

```
mysql -u root -p
Code language: SQL (Structured Query Language) (sql)
```

It will prompt for a password. You type the password to connect the MariaDB server:

```
Enter password: ********    
Code language: SQL (Structured Query Language) (sql)
```

Once you are connected, you will see a welcome screen with the following command-line:

```
mysql>
Code language: SQL (Structured Query Language) (sql)
```

Now, you can start using any SQL statement. For example, you can show all databases in the current server using the `[show databases](https://www.mariadbtutorial.com/mariadb-basics/mariadb-show-databases/)` command as follows:

```
mysql> show databases;
Code language: SQL (Structured Query Language) (sql)
```

Here is the output that shows the default databases:

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test               |
+--------------------+
4 rows in set (0.01 sec)
Code language: SQL (Structured Query Language) (sql)
```

## Connecting to the MariaDB server on a specific host

To connect to MariaDB on a specific host, you use the `-h` option:

```
mysql -u [username] -p[password] -h [hostname]
Code language: SQL (Structured Query Language) (sql)
```

For example, the following command connects to the MariaDB server with IP `172.16.13.5` using the `root` account:

```
mysql -u root -p -h 172.16.13.5
Code language: SQL (Structured Query Language) (sql)
```

It will also prompt for a password:

```
Enter password: ********    
Code language: SQL (Structured Query Language) (sql)
```

Note that the root account must be enabled for remote access in this case.

## Connecting to a specific database on the MariaDB server

To connect to a specific database, you specify the database name after all the options:

```
mysql -u [username] -p[password] -h [hostname] database_name
Code language: SQL (Structured Query Language) (sql)
```

The following command connects to the `information_schema` database of the MariaDB server on the `localhost`:

```
mysql -u root -p -h localhost information_schema
Enter password: ********
Code language: SQL (Structured Query Language) (sql)
```
