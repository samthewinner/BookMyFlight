import { Eureka } from 'eureka-js-client';
import path from 'path';
import dotenv from "dotenv";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, "./.env") });

const eurekaHost = process.env.EUREKA_CLIENT_SERVICEURL_DEFAULTZONE || 'eureka-server';
console.log(eurekaHost);

const eurekaPort = 8761;
const hostName = process.env.HOSTNAME || 'localhost';
const ipAddr = '127.0.0.1';
const instanceId = `${hostName}:${process.env.APP_NAME}-${process.env.PORT}`

export function registerWithEureka(appName, PORT) {
    const client = new Eureka({
        instance: {
            app: appName,
            instanceId: instanceId,
            port: {
                '$': PORT,
                '@enabled': true,
            },
            vipAddress: appName,
            dataCenterInfo: {
                '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
                name: 'MyOwn',
            },
        },
        eureka: {
            host: eurekaHost,
            port: eurekaPort,
            servicePath: '/eureka/apps/',
            maxRetries: 5,
            requestRetryDelay: 2000,
        },
    });


    client.start((error) => {
        console.log(error || "user service registered");
    });

    function exitHandler(options, exitCode) {
        if (options.cleanup) {

        }
        if (exitCode || exitCode === 0) {
            console.log(exitCode);
        }
        if (options.exit) {
            client.stop();
        }
    }

    process.on('SIGINT', () => exitHandler({ exit: true }));
}


