use ssh2::Session;
use std::fs;
use std::io::prelude::*;
use std::net::TcpStream;
use std::path::Path;
use serde::Deserialize;

#[derive(Debug,Deserialize)]
struct SshConfig {
    host: String,
    user: String,
    pwd: String,
    port: String,
    cmd: String,
}

fn read_config<P: AsRef<Path>>(path: P) -> Option<SshConfig> {
    let config_content = fs::read_to_string(path).ok()?;
    let config: SshConfig = toml::de::from_str(&config_content).ok()?;
    Some(config)
    
}

fn main() {
    let config_path = "config.toml";
    let config = read_config(config_path).unwrap_or_else(|| {

        SshConfig {
            host: "127.0.0.1".to_string(),
            user: "root".to_string(),
            pwd: "pwd".to_string(),
            port: "22".to_string(),
            cmd: "docker-compose restart *".to_string(),
        }
    });
    

    let addr = format!("{}:{}", config.host, config.port);
   
    match TcpStream::connect(addr) {
        Ok(tcp) =>{
           
            let mut sess= Session::new().unwrap();
            sess.set_tcp_stream(tcp);
            sess.handshake().unwrap();
            sess.userauth_password(&config.user, &config.pwd).unwrap();

            let mut chan = sess.channel_session().unwrap();
            chan.exec(&format!("{}", config.cmd)).unwrap();

            let mut s = String::new();
            chan.read_to_string(&mut s).unwrap();
            println!("执行结果:{}",s);
            

            chan.wait_close().unwrap();
            chan.exit_status().unwrap();
            println!("重新传输数据");
        }
        Err(e) => {
            println!("错误:{}",e);
        }
    } 

    println!("任意按键关闭窗口.....");
    let _ = std::io::stdin().read_line(&mut String::new());

}
