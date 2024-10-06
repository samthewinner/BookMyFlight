package com.example.jwt_api_gateway.filter;

import com.example.jwt_api_gateway.util.JwtUtil;
import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class AuthenticationFilter extends AbstractGatewayFilterFactory<AuthenticationFilter.Config> {

    @Autowired
    private JwtUtil jwtUtil;

    
    @Autowired
    private RouteValidator validator;

    public AuthenticationFilter() {
        super(Config.class);
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            if(validator.isSecured.test(exchange.getRequest())){            
                if (!exchange.getRequest().getHeaders().containsKey(HttpHeaders.AUTHORIZATION)) {
                    return onError(exchange, "No Authorization header", HttpStatus.UNAUTHORIZED);
                }

                String authHeader = exchange.getRequest().getHeaders().get(HttpHeaders.AUTHORIZATION).get(0);
                String token = authHeader.replace("Bearer ", "").trim();

                try {
                    System.out.println("Before claims");
                    Claims claims = jwtUtil.validateToken(token);
                    // System.out.println("After claims");
                    // System.out.println("Claims: " + claims);
                    String role = claims.get("role", String.class);
                    // System.out.println("Roles: " + role );
                    if(role.equals("admin"))
                        {
                            // System.out.println("Admin ID: " + claims.get("id", String.class));
                            return chain.filter(exchange.mutate().request(
                        exchange.getRequest().mutate()
                            .header("adminId", claims.get("id", String.class))
                            .header("role", claims.get("role", String.class))
                            .headers(headers -> headers.remove(HttpHeaders.AUTHORIZATION))  // Strip the Authorization header
                            .build()
                    ).build());
                        }
                    
                    System.out.println("User ID: " + claims.get("userid", String.class));


                    // Add the claims as headers
                    return chain.filter(exchange.mutate().request(
                        exchange.getRequest().mutate()
                            .header("userId", claims.get("userid", String.class))
                            .header("role", claims.get("role", String.class))
                            .headers(headers -> headers.remove(HttpHeaders.AUTHORIZATION))  // Strip the Authorization header
                            .build()
                    ).build());
                } catch (Exception e) {
                    System.out.println("Invalid access: " + e.getMessage());
                    return onError(exchange, "Unauthorized access to application: " + e.getMessage(), HttpStatus.UNAUTHORIZED);
                }
            }
            return chain.filter(exchange);
        };
    }

    private Mono<Void> onError(ServerWebExchange exchange, String err, HttpStatus httpStatus) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(httpStatus);
        return response.writeWith(Mono.just(response.bufferFactory().wrap(err.getBytes())));
    }

    public static class Config {
        // Config properties if needed
    }
}